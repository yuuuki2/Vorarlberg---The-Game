from flask import Flask, jsonify, send_from_directory, request
import mysql.connector
import os
import pickle
from shapely.geometry import mapping

app = Flask(__name__, static_folder='.')

# MariaDB connection parameters
DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'vtg_data'
}

def get_db_connection():
    """Create and return a connection to the MariaDB database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MariaDB: {err}")
        return None

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Add a route to serve image files
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/stops/<int:game_step>')
def get_stops(game_step):
    # Ensure game_step is between 0 and 7
    game_step = max(0, min(game_step, 7))
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    cursor = conn.cursor()
    
    # Get all stops that are included in the current game step
    cursor.execute(f"""
        SELECT 
            s.id, s.name, s.lat, s.lon, s.bezirk, s.gemeinde, s.altitude
        FROM ro_stops s
        INNER JOIN vtg_livedemo l ON s.id = l.stop_id
        WHERE l.included_{game_step} = 1
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    stops = [
        {
            'id': stop_id,
            'name': name,
            'lat': lat,
            'lon': lon,
            'bezirk': bezirk,
            'gemeinde': gemeinde,
            'altitude': altitude
        }
        for stop_id, name, lat, lon, bezirk, gemeinde, altitude in rows
    ]
    
    return jsonify(stops)

@app.route('/poi/<poi_type>')
def get_poi(poi_type):
    """Get points of interest of a specific type"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, lat, lon
        FROM ro_points_of_interest
        WHERE type = %s
    """, (poi_type,))
    
    rows = cursor.fetchall()
    conn.close()
    
    pois = [
        {
            'id': poi_id,
            'name': name,
            'lat': lat,
            'lon': lon
        }
        for poi_id, name, lat, lon in rows
    ]
    
    return jsonify(pois)

@app.route('/boundaries/<boundary_type>.json')
def get_boundaries(boundary_type):
    if boundary_type not in ['bundesland', 'bezirk', 'gemeinde']:
        return jsonify({"error": "Invalid boundary type"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    cursor = conn.cursor()
    # MariaDB uses %s as placeholder
    cursor.execute("""
        SELECT name, shape_data
        FROM ro_boundaries
        WHERE type = %s
    """, (boundary_type,))
    
    features = []
    for name, shape_data in cursor.fetchall():
        shape = pickle.loads(shape_data)
        geometry = mapping(shape)  # Convert to GeoJSON format
        
        features.append({
            "type": "Feature",
            "properties": {
                "name": name,
                "type": boundary_type
            },
            "geometry": geometry
        })
    
    conn.close()
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    

if __name__ == '__main__':
    app.run(debug=True, port=7042)