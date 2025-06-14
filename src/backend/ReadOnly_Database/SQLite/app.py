#Dieser Code wurde mit ChatGPT erstellt, um die Daten auus der Bushaltestellen-Datenbank zu visualisiern und so die Richtigkeit der Daten zu prüfen
#Genauer Prompt nicht mehr verfügbar, da ich meinen Chatverlauf gelöscht habe. Ungefährer Wortlaut nächste Zeile
#Prompt: Create a Flask app that uses Leaflet to visualize the data, including Gemeinde, Bezirk, Altitude and Bus Routes of every stop
#Prompt 2: please add a way of visualising the boundaries in the app.py. There should be an option to switch between vorarlberg, bezirk, and gemeinde boundaries, and to toggle bus station visibility
#Prompt 3: now add support in app.py for displaying PoI. they should be toggleable like bus stops. they should all have different collors to bus stops and each other. when hovering, they should display name and type
#Prompt 4: Add a slider and a selector where i can select to only display stops within x kilometers of a mountain/train station etc. Should also be toggleable to display all bus stops like regular

from flask import Flask, jsonify, send_from_directory
import sqlite3
import os
import pickle
from shapely.geometry import mapping

app = Flask(__name__, static_folder='.')

DB_PATH = os.path.join(os.path.dirname(__file__), 'RO_GeoData.db')

@app.route('/stops.json')
def get_stops():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.name, s.lat, s.lon, s.bezirk, s.gemeinde, s.altitude,
            s.distance_trainstation, s.distance_mountain, s.distance_minigolf, s.distance_museum,
            GROUP_CONCAT(r.name, ', ') AS routes
        FROM stops s
        LEFT JOIN stops_routes sr ON s.id = sr.stop_id
        LEFT JOIN routes r ON sr.route_id = r.id
        GROUP BY s.id
        
    """)
    rows = cursor.fetchall()
    conn.close()
    stops = [
        {
            'name': name,
            'lat': lat,
            'lon': lon,
            'bezirk': bezirk,
            'gemeinde': gemeinde,
            'altitude': altitude,
            'distance_trainstation': distance_trainstation,
            'distance_mountain': distance_mountain,
            'distance_minigolf': distance_minigolf,
            'distance_museum': distance_museum,
            'routes': routes if routes else 'None'
        }
        for name, lat, lon, bezirk, gemeinde, altitude, distance_trainstation, distance_mountain, distance_minigolf, distance_museum, routes in rows
    ]
    return jsonify(stops)

@app.route('/boundaries/<boundary_type>.json')
def get_boundaries(boundary_type):
    if boundary_type not in ['bundesland', 'bezirk', 'gemeinde']:
        return jsonify({"error": "Invalid boundary type"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, shape_data
        FROM boundaries
        WHERE type = ?
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
    
    return jsonify(geojson)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/poi.json')
def get_poi():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id, name, lat, lon, type
        FROM points_of_interest
    """)
    rows = cursor.fetchall()
    conn.close()
    
    poi = [
        {
            'id': poi_id,
            'name': name,
            'lat': lat,
            'lon': lon,
            'type': poi_type
        }
        for poi_id, name, lat, lon, poi_type in rows
    ]
    return jsonify(poi)



if __name__ == '__main__':
    app.run(debug=True, port=6969)
