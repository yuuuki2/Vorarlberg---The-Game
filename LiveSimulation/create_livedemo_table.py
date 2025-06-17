import mysql.connector
import pickle
from math import radians, cos, sin, asin, sqrt
from shapely.geometry import Point, shape, mapping

# MariaDB connection parameters
DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'vtg_data'
}

def haversine(lon1, lat1, lon2, lat2):
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
    r = 6371  # Radius of earth in kilometers
    return c * r

def is_in_bezirk_bregenz(conn, lat, lon):
    """Check if a point is within Bezirk Bregenz boundary"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT shape_data FROM ro_boundaries 
        WHERE type = 'bezirk' AND name = 'Bregenz'
    """)
    row = cursor.fetchone()
    
    if not row:
        return False
    
    bregenz_shape = pickle.loads(row[0])
    point = Point(lon, lat)  # Note: shapely uses (lon, lat) order
    
    return bregenz_shape.contains(point)


def calculate_distances(conn, step_km=2):
    """
    Calculate distances from each bus stop to the nearest train station.
    Round distances to the nearest step_km kilometers.
    """
    cursor = conn.cursor()
    
    # Get all train stations
    cursor.execute("""
        SELECT lat, lon FROM ro_points_of_interest
        WHERE type = 'train_station'
    """)
    train_stations = cursor.fetchall()
    
    # Get all bus stops
    cursor.execute("SELECT id, lat, lon FROM ro_stops")
    bus_stops = cursor.fetchall()
    
    distances = {}
    
    for stop_id, stop_lat, stop_lon in bus_stops:
        # Find minimum distance to any train station
        min_distance = float('inf')
        for station_lat, station_lon in train_stations:
            dist = haversine(stop_lon, stop_lat, station_lon, station_lat)
            min_distance = min(min_distance, dist)
        
        # Round to nearest step_km
        rounded_distance = round(min_distance / step_km) * step_km
        distances[stop_id] = rounded_distance
    
    return distances



def compare_distances_to_points(conn, point1_lat, point1_lon, point2_lat, point2_lon, from_step, to_step, closer_to_which_point_gets_excluded):
    """
    Compare the distance from each bus stop to two points and update inclusion status.
    
    Args:
        conn: Database connection
        point1_lat, point1_lon: Coordinates of first point
        point2_lat, point2_lon: Coordinates of second point
        from_step: Source step to copy from
        to_step: Target step to update
        closer_to_which_point_gets_excluded: 1 or 2, indicating which point's proximity causes exclusion
    """
    cursor = conn.cursor()
    
    # Copy values from source step to target step
    cursor.execute(f"UPDATE vtg_livedemo SET included_{to_step} = included_{from_step}")
    
    # Get all bus stops with their coordinates
    cursor.execute("SELECT id, lat, lon FROM ro_stops")
    stops = cursor.fetchall()
    
    # Calculate and compare distances for each stop
    for stop_id, stop_lat, stop_lon in stops:
        dist1 = haversine(stop_lon, stop_lat, point1_lon, point1_lat)
        dist2 = haversine(stop_lon, stop_lat, point2_lon, point2_lat)
        
        # Set to 0 based on which point should cause exclusion when closer
        if (closer_to_which_point_gets_excluded == 2 and dist2 < dist1) or \
           (closer_to_which_point_gets_excluded == 1 and dist1 < dist2):
            cursor.execute(f"""
                UPDATE vtg_livedemo SET included_{to_step} = 0
                WHERE stop_id = %s
            """, (stop_id,))

try:
    # Connect to the database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Create the vtg_livedemo table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vtg_livedemo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        stop_id VARCHAR(255),
        included_0 BOOLEAN DEFAULT 1,
        included_1 BOOLEAN DEFAULT 0,
        included_2 BOOLEAN DEFAULT 0,
        included_3 BOOLEAN DEFAULT 0,
        included_4 BOOLEAN DEFAULT 0,
        included_5 BOOLEAN DEFAULT 0,
        included_6 BOOLEAN DEFAULT 0,
        included_7 BOOLEAN DEFAULT 0,
        FOREIGN KEY (stop_id) REFERENCES ro_stops(id)
    ) ENGINE=InnoDB
    """)
    
    # Check if we need to initialize the table with data
    cursor.execute("SELECT COUNT(*) FROM vtg_livedemo")
    count = cursor.fetchone()[0]
    
    # If table is empty, populate it with all stops from ro_stops
    if count == 0:
        cursor.execute("SELECT id FROM ro_stops")
        stops = cursor.fetchall()
        
        for stop in stops:
            cursor.execute("""
            INSERT INTO vtg_livedemo (stop_id, included_0)
            VALUES (%s, 1)
            """, (stop[0],))
    
    conn.commit()
    print("Successfully created and initialized vtg_livedemo table")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
    
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        
        
        
        
try:
    # Connect to the database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Step 0: Set all to 1 (this is already done when table is created)
    print("Processing step 0: All stops included.")
    
    # Step 1: Copy from 0, then set all bus stops within 10km of [47.417157, 9.738644] to 0
    print("Processing step 1: Excluding stops within 10km of [47.417157, 9.738644]...")
    seeker_lat, seeker_lon = 47.417157, 9.738644
    
    cursor.execute("SELECT stop_id, included_0 FROM vtg_livedemo")
    stops = cursor.fetchall()
    
    # First copy values from included_0 to included_1
    cursor.execute("UPDATE vtg_livedemo SET included_1 = included_0")
    
    # Then get all bus stops with their coordinates
    cursor.execute("SELECT id, lat, lon FROM ro_stops")
    all_stops = {stop_id: (lat, lon) for stop_id, lat, lon in cursor.fetchall()}
    
    # Set included_1 = 0 for stops within 10km
    for stop_id, inc_0 in stops:
        if stop_id in all_stops:
            lat, lon = all_stops[stop_id]
            distance = haversine(lon, lat, seeker_lon, seeker_lat)
            if distance <= 10:
                cursor.execute("""
                    UPDATE vtg_livedemo SET included_1 = 0
                    WHERE stop_id = %s
                """, (stop_id,))
    
    # Step 2: Copy from 1, set all to 0 that are further from [47.417157, 9.738644] than from [47.412526, 9.731503]
    print("Processing step 2: Applying perpendicular line filter...")
    point1_lat, point1_lon = 47.417157, 9.738644
    point2_lat, point2_lon = 47.412526, 9.731503
    
    # Use the new function for step 2 - exclude stops closer to point2
    compare_distances_to_points(
        conn, 
        point1_lat, point1_lon, 
        point2_lat, point2_lon, 
        from_step=1, 
        to_step=2, 
        closer_to_which_point_gets_excluded=2
    )
    
    # Step 3: Copy from 2, set all stops with altitude < 424m to 0
    print("Processing step 3: Excluding stops with altitude below 424m...")
    
    # Copy values from included_2 to included_3
    cursor.execute("UPDATE vtg_livedemo SET included_3 = included_2")
    
    # Get all bus stops with their altitudes
    cursor.execute("SELECT id, altitude FROM ro_stops")
    stop_altitudes = {stop_id: altitude for stop_id, altitude in cursor.fetchall()}
    
    for stop_id, altitude in stop_altitudes.items():
        if altitude is not None and altitude < 424:
            cursor.execute("""
                UPDATE vtg_livedemo SET included_3 = 0
                WHERE stop_id = %s
            """, (stop_id,))
    
    # Step 4: Copy from 3
    print("Processing step 4: Copying from step 3...")
    cursor.execute("UPDATE vtg_livedemo SET included_4 = included_3")
    
    # Step 5: Copy from 4, set all to 0 which are not 4km away from train stations
    print("Processing step 5: Filtering by distance to train stations...")
    
    # Copy values from included_4 to included_5
    cursor.execute("UPDATE vtg_livedemo SET included_5 = included_4")
    
    # Calculate distances to nearest train station
    distances = calculate_distances(conn, step_km=2)
    
    for stop_id, distance in distances.items():
        if distance != 4:  # Keep only stops that are 4km (rounded to nearest 2km) from train stations
            cursor.execute("""
                UPDATE vtg_livedemo SET included_5 = 0
                WHERE stop_id = %s
            """, (stop_id,))
    
    # Step 6: Copy from 5, set all points to 0 that are further from [47.438056, 9.756982] than from [47.451746, 9.820544]
    print("Processing step 6: Applying perpendicular line filter for new points...")
    point1_lat, point1_lon = 47.438056, 9.756982
    point2_lat, point2_lon = 47.451746, 9.820544
    
    # Use the new function for step 6 - exclude stops closer to point1
    compare_distances_to_points(
        conn, 
        point1_lat, point1_lon, 
        point2_lat, point2_lon, 
        from_step=5, 
        to_step=6, 
        closer_to_which_point_gets_excluded=1
    )
    
    # Step 7: Set all to 0, except bus station with id 3650525914
    print("Processing step 7: Final step - only showing target bus stop...")
    
    # Set all to 0 first
    cursor.execute("UPDATE vtg_livedemo SET included_7 = 0")
    
    # Then set the specific bus stop to 1
    cursor.execute("""
        UPDATE vtg_livedemo SET included_7 = 1
        WHERE stop_id = '3650525914'
    """)
    
    conn.commit()
    print("Successfully updated vtg_livedemo table for all steps!")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
    
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()

