#Dieser Code wurde mit ChatGPT erstellt, um eine Datenbank mit allen Bushaltestellen Vorarlbergs zu erstellen
#Genauer Prompt nicht mehr verfügbar, da ich meinen Chatverlauf gelöscht habe. Ungefährer Wortlaut nächste Zeile
#Prompt: Using OpenStreetMap, Python and SQLite, create a database of all bus stops in Vorarlberg including their Bezirk and Gemeinde, altitude, and Bus Routes stopping at each station. Save the routes in a separate table and use a M-M connection Table.
#Prompt 2: Add a new table to the db where the outlines of vorarlberg, all the bezirke and al the gemeniden is stored. It should follow id, name (i.e. Vorarlberg, Schruns, Dornbirn), type(bundesland, bezirk, gemeinde), shape_data. It should be saved in a way so it can be retrieved later to perform checks in which region a specific coordinate is. The data should be retrieved from osm.
#Prompt 3: Add four more rows to the bus stop table: distance_trainstation, distance_mountain, distance_minigolf, distance_museum. Then add a function that adds the distance to the nearest train station, mountain, minigolf and museum to every bus stop, rounded to be within x kilometer steps
#Prompt 4: Convert this entire File to use MariaDB. the user is root, with password root. Also add a new user to MariaDB with the name vtg_server that has read-only access to the database ro_geodata. The password for this user is vtg_server.

import requests
import mysql.connector  # Changed from sqlite3 to mysql.connector
import geopandas as gpd
from shapely.geometry import Point, shape
import pickle
from create_info_db import main as create_info_db_main


# Constants
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
ALTITUDE_API_URL = "https://api.open-elevation.com/api/v1/lookup"
VORARLBERG_BOUNDARY_QUERY = """
[out:json];
relation["name"="Vorarlberg"]["admin_level"="4"];
out geom;
"""

# MariaDB connection parameters
DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'vtg_data'
}

# Initialize DB
def init_db():
    # First connect without specifying a database to create it if needed
    conn = mysql.connector.connect(
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host']
    )
    c = conn.cursor()
    
    # Create database if it doesn't exist
    c.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    conn.close()
    
    # Connect to the database
    conn = mysql.connector.connect(**DB_CONFIG)
    c = conn.cursor()
    
    # Create tables with MariaDB syntax
    c.execute("""
    CREATE TABLE IF NOT EXISTS ro_stops (
        id VARCHAR(255) PRIMARY KEY,
        name TEXT,
        lat FLOAT,
        lon FLOAT,
        altitude FLOAT,
        bezirk TEXT,
        gemeinde TEXT,
        distance_trainstation FLOAT,
        distance_mountain FLOAT,
        distance_minigolf FLOAT,
        distance_museum FLOAT
    ) ENGINE=InnoDB
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS ro_routes (
        id VARCHAR(255) PRIMARY KEY,
        name TEXT
    ) ENGINE=InnoDB
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS ro_stops_routes (
        stop_id VARCHAR(255),
        route_id VARCHAR(255),
        PRIMARY KEY (stop_id, route_id),
        FOREIGN KEY (stop_id) REFERENCES ro_stops(id),
        FOREIGN KEY (route_id) REFERENCES ro_routes(id)
    ) ENGINE=InnoDB
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS ro_boundaries (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name TEXT,
        type TEXT,
        shape_data LONGBLOB
    ) ENGINE=InnoDB
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS ro_points_of_interest (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name TEXT,
        lat FLOAT,
        lon FLOAT,
        type TEXT
    ) ENGINE=InnoDB
    """)
    
    conn.commit()
    
    # Prompt: Please modify this code to grant the newly created user full privileges to vtg_, but only allow him to read any table with prefix ro_
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        c = conn.cursor()

        # Drop user if exists
        c.execute("DROP USER IF EXISTS 'vtg_server'@'localhost'")

        # Create user
        c.execute("CREATE USER 'vtg_server'@'localhost' IDENTIFIED BY 'vtg_server'")

        # Get all tables starting with vtg_
        c.execute(f"""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = %s AND table_name LIKE 'vtg_%'
        """, (DB_CONFIG['database'],))
        vtg_tables = c.fetchall()

        # Grant full DML privileges on vtg_ tables
        for (table_name,) in vtg_tables:
            c.execute(f"""
                GRANT SELECT, INSERT, UPDATE, DELETE ON `{DB_CONFIG['database']}`.`{table_name}` TO 'vtg_server'@'localhost'
            """)

        # Get all ro_ tables
        c.execute(f"""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = %s AND table_name LIKE 'ro_%'
        """, (DB_CONFIG['database'],))
        ro_tables = c.fetchall()

        # Grant only SELECT on ro_ tables
        for (table_name,) in ro_tables:
            c.execute(f"""
                GRANT SELECT ON `{DB_CONFIG['database']}`.`{table_name}` TO 'vtg_server'@'localhost'
            """)

        # Flush privileges
        c.execute("FLUSH PRIVILEGES")
        conn.commit()

        print("User 'vtg_server' created with correct privileges.")

    except mysql.connector.Error as err:
        print(f"Error configuring user permissions: {err}")
            
    conn.commit()
    return conn

# Get Vorarlberg exact boundary as shapely polygon
def get_vorarlberg_boundary():
    # Request relation with all ways
    query = """
    [out:json][timeout:60];
    relation["name"="Vorarlberg"]["admin_level"="4"];
    (._;>;);
    out body;
    """
    response = requests.get(OVERPASS_URL, params={'data': query})
    data = response.json()

    # Separate nodes and ways
    nodes = {el['id']: el for el in data['elements'] if el['type'] == 'node'}
    ways = [el for el in data['elements'] if el['type'] == 'way']

    # Build a list of coordinate rings from way nodes
    lines = []
    for way in ways:
        coords = []
        for node_id in way['nodes']:
            node = nodes.get(node_id)
            if node:
                coords.append((node['lon'], node['lat']))
        if coords:
            lines.append(coords)

    # Attempt to build a polygon from the lines
    from shapely.ops import linemerge, polygonize
    from shapely.geometry import LineString

    merged = linemerge([LineString(line) for line in lines])
    polygons = list(polygonize(merged))
    if polygons:
        return polygons[0]  # Use the first polygon (mainland)
    else:
        return None

# Get all bus stops in bounding box
def get_bus_stops(bbox):
    query = f"""
    [out:json][timeout:60];
    node["highway"="bus_stop"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
    out body;
    """
    response = requests.get(OVERPASS_URL, params={'data': query})
    return response.json()["elements"]

def fetch_altitude(lat, lon):
    response = requests.get(ALTITUDE_API_URL, params={"locations": f"{lat},{lon}"})
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0].get("elevation", None)
    return None

# Filter stops within exact boundary and store in DB
def store_stops_within_boundary(stops, boundary, conn):
    c = conn.cursor()
    for stop in stops:
        pt = Point(stop['lon'], stop['lat'])
        if boundary.contains(pt):
            stop_name = stop['tags'].get('name', 'Unknown')
            
            # Check if a stop with the same name already exists
            c.execute("SELECT COUNT(*) FROM ro_stops WHERE name = %s", (stop_name,))
            if c.fetchone()[0] > 0:
                continue  # Skip adding this stop if a duplicate name exists
            
            # MariaDB uses %s placeholders instead of ?
            c.execute("""
                INSERT IGNORE INTO ro_stops (id, name, lat, lon)
                VALUES (%s, %s, %s, %s)
            """, (str(stop['id']), stop_name, stop['lat'], stop['lon']))
    conn.commit()

# Load admin regions (Bezirke + Gemeinden) from Overpass
def get_admin_boundaries(level):
    print(f"Fetching admin_level {level} boundaries...")
    query = f"""
    [out:json][timeout:90];
    area["name"="Vorarlberg"]->.searchArea;
    relation["admin_level"="{level}"](area.searchArea);
    (._;>;);
    out body;
    """
    response = requests.get(OVERPASS_URL, params={'data': query})
    data = response.json()

    nodes = {el['id']: el for el in data['elements'] if el['type'] == 'node'}
    ways = [el for el in data['elements'] if el['type'] == 'way']
    relations = [el for el in data['elements'] if el['type'] == 'relation']

    from shapely.ops import linemerge, polygonize
    from shapely.geometry import LineString

    features = []
    for rel in relations:
        rel_ways = [w for w in ways if w['id'] in [m['ref'] for m in rel.get('members', []) if m['type'] == 'way']]
        lines = []
        for way in rel_ways:
            coords = []
            for node_id in way['nodes']:
                node = nodes.get(node_id)
                if node:
                    coords.append((node['lon'], node['lat']))
            if coords:
                lines.append(coords)
        if not lines:
            continue
        merged = linemerge([LineString(line) for line in lines])
        polygons = list(polygonize(merged))
        if polygons:
            features.append({'name': rel['tags'].get('name', 'Unknown'), 'geometry': polygons[0]})
    print(f"Loaded {len(features)} admin regions for level {level}")
    return features


def store_boundaries(conn, boundary, bezirke, gemeinden):
    print("Storing boundaries in database...")
    c = conn.cursor()
    
    # Store Vorarlberg boundary
    vorarlberg_shape = pickle.dumps(boundary)
    c.execute("""
    INSERT INTO ro_boundaries (name, type, shape_data)
    VALUES (%s, %s, %s)
    """, ('Vorarlberg', 'bundesland', vorarlberg_shape))
    
    # Store Bezirke boundaries
    for bezirk in bezirke:
        bezirk_shape = pickle.dumps(bezirk['geometry'])
        c.execute("""
        INSERT INTO ro_boundaries (name, type, shape_data)
        VALUES (%s, %s, %s)
        """, (bezirk['name'], 'bezirk', bezirk_shape))
    
    # Store Gemeinden boundaries
    for gemeinde in gemeinden:
        gemeinde_shape = pickle.dumps(gemeinde['geometry'])
        c.execute("""
        INSERT INTO ro_boundaries (name, type, shape_data)
        VALUES (%s, %s, %s)
        """, (gemeinde['name'], 'gemeinde', gemeinde_shape))
    
    conn.commit()
    print(f"Stored boundaries for 1 bundesland, {len(bezirke)} bezirke, and {len(gemeinden)} gemeinden.")


# Update DB entries with admin region info
def annotate_stops(conn, bezirke, gemeinden):
    c = conn.cursor()
    c.execute("SELECT id, lat, lon FROM ro_stops")
    stops = c.fetchall()
    for stop_id, lat, lon in stops:
        pt = Point(lon, lat)
        bezirk_name = next((b['name'] for b in bezirke if b['geometry'].contains(pt)), None)
        gemeinde_name = next((g['name'] for g in gemeinden if g['geometry'].contains(pt)), None)
        c.execute("""
            UPDATE ro_stops
            SET bezirk = %s, gemeinde = %s
            WHERE id = %s
        """, (bezirk_name, gemeinde_name, stop_id))
    conn.commit()


def clean_stop_names(conn):
    c = conn.cursor()
    c.execute("SELECT id, name, gemeinde FROM ro_stops WHERE gemeinde IS NOT NULL")
    updates = 0
    for stop_id, name, gemeinde in c.fetchall():
        if not name or not gemeinde:
            continue

        # Check if the name starts with the Gemeinde name (case-insensitive)
        if name.lower().startswith(gemeinde.lower()):
            # Remove the Gemeinde prefix from the stop name
            new_name = name[len(gemeinde):].strip()
            if new_name:  # Avoid empty name after removal
                c.execute("UPDATE ro_stops SET name = %s WHERE id = %s", (new_name, stop_id))
                updates += 1
    conn.commit()
    print(f"Cleaned {updates} stop names by removing Gemeinde prefix.")


# Function to fetch bus routes and their stops
def get_bus_routes_and_stops(bbox):
    query = f"""
    [out:json][timeout:60];
    relation["route"="bus"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
    (._;>;);
    out body;
    """
    response = requests.get(OVERPASS_URL, params={'data': query})
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Overpass API request failed with status code {response.status_code}")
        print(f"Response text: {response.text}")
        return {}, []

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print("Error: Failed to decode JSON response from Overpass API.")
        print(f"Response text: {response.text}")
        return {}, []

    if "elements" not in data:
        print("Warning: No elements found in Overpass API response.")
        return {}, []

    routes = {}
    stops_routes = []

    for rel in data['elements']:
        if rel['type'] == 'relation' and 'tags' in rel and 'name' in rel['tags']:
            route_id = rel['id']
            route_name = rel['tags']['name']
            routes[route_id] = route_name

            for member in rel.get('members', []):
                # Include nodes with role 'stop', 'platform', 'terminus', or no role
                if member['type'] == 'node' and member.get('role') in ['stop', 'platform', 'terminus', None]:
                    stops_routes.append((member['ref'], route_id))  # Use stop ID instead of name

    return routes, stops_routes

# Function to store routes and stops_routes in the database
def store_routes_and_stops_routes(routes, stops_routes, conn):
    c = conn.cursor()

    # Insert routes
    for route_id, route_name in routes.items():
        c.execute("""
        INSERT IGNORE INTO ro_routes (id, name)
        VALUES (%s, %s)
        """, (str(route_id), route_name))

    # Insert stops_routes only if the stop exists in the database
    print(f"STARTING TO INSERT STOPS ROUTES {len(stops_routes)}")
    for stop_id, route_id in stops_routes:
        # Check if the stop exists in the database
        c.execute("SELECT 1 FROM ro_stops WHERE id = %s", (str(stop_id),))
        if c.fetchone():  # Stop exists
            c.execute("""
            INSERT IGNORE INTO ro_stops_routes (stop_id, route_id)
            VALUES (%s, %s)
            """, (str(stop_id), str(route_id)))

    conn.commit()

# Function to calculate and update altitude for all stops
def update_altitudes(conn):
    c = conn.cursor()
    c.execute("SELECT id, lat, lon FROM ro_stops WHERE altitude IS NULL")
    stops = c.fetchall()
    print(f"Updating altitude for {len(stops)} stops...")
    
    i = 0
    for stop_id, lat, lon in stops:
        i += 1
        if i % 100 == 0:
            print(f"Processed {i} stops...")
        altitude = fetch_altitude(lat, lon)
        c.execute("""
            UPDATE ro_stops
            SET altitude = %s
            WHERE id = %s
        """, (altitude, stop_id))
    conn.commit()
    print("Altitude update complete.")

# Function to remove routes with 1 or 0 stops
def remove_routes_with_few_stops(conn):
    c = conn.cursor()

    # Find routes with 1 or 0 stops
    c.execute("""
    SELECT r.id
    FROM ro_routes r
    LEFT JOIN ro_stops_routes sr ON r.id = sr.route_id
    GROUP BY r.id
    HAVING COUNT(sr.stop_id) <= 1
    """)
    routes_to_remove = [row[0] for row in c.fetchall()]

    if routes_to_remove:
        print(f"Removing {len(routes_to_remove)} routes with 1 or 0 stops...")

        # Remove entries from stops_routes
        for route_id in routes_to_remove:
            c.execute("DELETE FROM ro_stops_routes WHERE route_id = %s", (route_id,))

        # Remove entries from routes
        for route_id in routes_to_remove:
            c.execute("DELETE FROM ro_routes WHERE id = %s", (route_id,))

        conn.commit()
        print("Routes with 1 or 0 stops removed.")
    else:
        print("No routes with 1 or 0 stops found.")


def populate_poi(conn, boundary):
    print("Creating and populating Points of Interest table...")
    c = conn.cursor()
    
    # Clear existing POIs to avoid duplicates when re-running
    c.execute("DELETE FROM ro_points_of_interest")
    conn.commit()
    
    # Define types and their OSM tags - expanded to catch more variations
    poi_types = {
        'train_station': [
            {'railway': 'station'},
            {'railway': 'halt'},
            {'railway': 'stop'},
            {'public_transport': 'station', 'train': 'yes'},
            {'public_transport': 'stop_position', 'train': 'yes'}
        ],
        'mountain': [
            {'natural': 'peak'},
            {'natural': 'mountain_range'}
        ],
        'minigolf_course': [
            {'leisure': 'miniature_golf'},
            {'sport': 'miniature_golf'},
            {'sport': 'minigolf'},
            {'leisure': 'golf', 'golf': 'miniature'},
            {'leisure': 'minigolf'},
            {'amenity': 'miniature_golf'},
            {'amenity': 'minigolf'},
            {'leisure': 'recreation_ground', 'sport': 'minigolf'},
            {'leisure': 'recreation_ground', 'sport': 'miniature_golf'}
        ],
        'museum': [
            {'tourism': 'museum'},
            {'amenity': 'museum'},
            {'building': 'museum'},
            {'historic': 'museum'}
        ]
    }
    
    bbox = boundary.bounds  # (minx, miny, maxx, maxy)
    
    # Fetch and store each type of POI with its variations
    for poi_type, tag_variations in poi_types.items():
        print(f"Fetching {poi_type}s from OSM...")
        all_elements = []
        
        for tags in tag_variations:
            # Build the tag query part
            tag_query = ""
            for tag_key, tag_value in tags.items():
                tag_query += f'["{tag_key}"="{tag_value}"]'
            
            # Node query
            node_query = f"""
            [out:json][timeout:60];
            node{tag_query}({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
            out body;
            """
            
            # For mountains, remove the (._;>;); part from the way query
            if poi_type == 'mountain':
                way_query = f"""
                [out:json][timeout:60];
                way{tag_query}({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
                out center;
                """
            else:
                way_query = f"""
                [out:json][timeout:60];
                way{tag_query}({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
                (._;>;);
                out center;
                """
            
            # Try both node and way queries
            for query in [node_query, way_query]:
                try:
                    response = requests.get(OVERPASS_URL, params={'data': query})
                    
                    if response.status_code != 200:
                        print(f"Error fetching {poi_type}s with query {query}: {response.status_code}")
                        continue
                        
                    data = response.json()
                    elements = data.get('elements', [])
                    
                    # For ways, extract the center point
                    for element in elements:
                        if element['type'] == 'way' and 'center' in element:
                            element['lat'] = element['center']['lat']
                            element['lon'] = element['center']['lon']
                    
                    # Filter to only include elements with lat and lon
                    elements = [e for e in elements if 'lat' in e and 'lon' in e]
                    
                    print(f"Found {len(elements)} {poi_type}s with tag variation {tags}")
                    all_elements.extend(elements)
                except Exception as e:
                    print(f"Error processing {poi_type}s with query {query}: {str(e)}")
        
        # Remove duplicates based on OSM ID
        seen_ids = set()
        unique_elements = []
        for element in all_elements:
            if element['id'] not in seen_ids:
                seen_ids.add(element['id'])
                unique_elements.append(element)
        
        print(f"Total unique {poi_type}s found: {len(unique_elements)}")
        
        # Insert into database
        for element in unique_elements:
            pt = Point(element['lon'], element['lat'])
            if boundary.contains(pt):
                name = element.get('tags', {}).get('name', f"Unnamed {poi_type}")
                c.execute("""
                INSERT IGNORE INTO ro_points_of_interest (name, lat, lon, type)
                VALUES (%s, %s, %s, %s)
                """, (name, element['lat'], element['lon'], poi_type))
    
    conn.commit()
    print("Points of Interest table populated successfully.")


def calculate_distances(conn, step_km=2):
    """
    Calculate distances from each bus stop to the nearest POI of each type.
    Round distances to the nearest step_km kilometers.
    """
    from math import radians, cos, sin, asin, sqrt
    
    def haversine(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        # Haversine formula
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        # Radius of earth in kilometers is 6371
        km = 6371 * c
        return km
    
    def round_to_step(distance, step):
        """Round distance to the nearest step kilometers"""
        return round(distance / step) * step
    
    c = conn.cursor()
    
    # Get all stops
    c.execute("SELECT id, lat, lon FROM ro_stops")
    stops = c.fetchall()
    total_stops = len(stops)
    print(f"Calculating distances for {total_stops} bus stops...")
    
    # Get POIs by type
    poi_types = ['train_station', 'mountain', 'minigolf_course', 'museum']
    poi_data = {}
    
    for poi_type in poi_types:
        c.execute("SELECT name, lat, lon FROM ro_points_of_interest WHERE type = %s", (poi_type,))
        poi_data[poi_type] = c.fetchall()
        print(f"Found {len(poi_data[poi_type])} {poi_type}s for distance calculation")
    
    # Calculate distances for each stop to each POI type
    for i, (stop_id, stop_lat, stop_lon) in enumerate(stops):
        if (i + 1) % 100 == 0 or (i + 1) == total_stops:
            print(f"Processed {i + 1}/{total_stops} stops")
        
        distances = {}
        
        for poi_type in poi_types:
            min_distance = float('inf')
            nearest_poi = None
            
            for poi_name, poi_lat, poi_lon in poi_data[poi_type]:
                distance = haversine(stop_lat, stop_lon, poi_lat, poi_lon)
                if distance < min_distance:
                    min_distance = distance
                    nearest_poi = poi_name
            
            # Handle case where no POI of this type exists
            if min_distance == float('inf'):
                distances[poi_type] = None
            else:
                # Round to the nearest step_km
                distances[poi_type] = round_to_step(min_distance, step_km)
        
        # Update the stop record with distances
        c.execute("""
            UPDATE ro_stops
            SET distance_trainstation = %s,
                distance_mountain = %s,
                distance_minigolf = %s,
                distance_museum = %s
            WHERE id = %s
        """, (
            distances['train_station'],
            distances['mountain'],
            distances['minigolf_course'],
            distances['museum'],
            stop_id
        ))
    
    conn.commit()
    print("Distance calculations complete")
    

def main():
    create_info_db_main()  # Create info database
    
    conn = init_db()
    print("Fetching Vorarlberg boundary...")
    boundary = get_vorarlberg_boundary()
    if boundary is None:
        print("Failed to fetch Vorarlberg boundary.")
        return

    print("Fetching bus stops...")
    bbox = boundary.bounds  # (minx, miny, maxx, maxy)
    stops = get_bus_stops(bbox)
    print(f"Fetched {len(stops)} stops. Filtering...")

    store_stops_within_boundary(stops, boundary, conn)

    print("Fetching Bezirke and Gemeinden boundaries...")
    bezirke = get_admin_boundaries("6")
    gemeinden = get_admin_boundaries("8")

    print("Storing boundaries for future use...")
    store_boundaries(conn, boundary, bezirke, gemeinden)
    
    print("Annotating stops with region data...")
    annotate_stops(conn, bezirke, gemeinden)

    print("Fetching bus routes and their stops...")
    routes, stops_routes = get_bus_routes_and_stops(bbox)
    store_routes_and_stops_routes(routes, stops_routes, conn)

    print("Updating altitudes for stops...")
    update_altitudes(conn)

    print("Cleaning stop names...")
    clean_stop_names(conn)

    print("Removing routes with 1 or 0 stops...")
    remove_routes_with_few_stops(conn)

    print("Populating Points of Interest...")
    populate_poi(conn, boundary)
    
    print("Calculating distances to Points of Interest...")
    calculate_distances(conn, step_km=2)
    
    print("Done.")
    

if __name__ == "__main__":
    main()