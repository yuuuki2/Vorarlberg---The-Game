"""! @file
@brief Controller module for the Vorarlberg The Game backend server.

This module implements all the controller functions for the game's API endpoints.
It handles game state management, player coordinates, questions, cards, and more.
"""

import connexion
import mysql.connector
import time
import json
import math
from typing import Dict, List, Tuple, Union
from math import radians, cos, sin, asin, sqrt

from openapi_server.models.bus_routes_get200_response_inner import BusRoutesGet200ResponseInner
from openapi_server.models.bus_stops_get200_response_inner import BusStopsGet200ResponseInner
from openapi_server.models.cards_get200_response_inner import CardsGet200ResponseInner
from openapi_server.models.curses_get200_response_inner import CursesGet200ResponseInner
from openapi_server.models.game_info_get200_response import GameInfoGet200Response
from openapi_server.models.hider_info_get200_response import HiderInfoGet200Response
from openapi_server.models.questions_current_get200_response import QuestionsCurrentGet200Response
from openapi_server.models.questions_get200_response_inner import QuestionsGet200ResponseInner
from openapi_server.models.questions_previous_get200_response_inner import QuestionsPreviousGet200ResponseInner
from openapi_server.models.seeker_get_coordinates_get200_response import SeekerGetCoordinatesGet200Response
from openapi_server.models.seeker_info_get200_response import SeekerInfoGet200Response
from openapi_server.models.seeker_post_coordinates_post_request import SeekerPostCoordinatesPostRequest
from openapi_server import util

##! Database configuration settings
DB_CONFIG = {
    'user': 'vtg_server',      ##!< Database user
    'password': 'vtg_server',  ##!< Database password
    'host': 'localhost',       ##!< Database host
    'database': 'vtg_data'     ##!< Database name
}

##! Global game state variables
GAME_STATE = {
    'is_started': False,       ##!< Flag indicating if game is in progress
    'start_time': None,        ##!< Game start time in Unix timestamp
    'hider_name': 'Hider',     ##!< Name of the hider player
    'seeker_name': 'Seeker'    ##!< Name of the seeker player
}

##! Global hider information
HIDER_INFO = {
    'lat': 47.4167,           ##!< Hider's latitude (default: Dornbirn)
    'lon': 9.7333,            ##!< Hider's longitude (default: Dornbirn)
    'bus_stop_id': None       ##!< ID of the bus stop where hider is hiding
}

##! Global seeker information
SEEKER_INFO = {
    'lat': 47.4167,           ##!< Seeker's latitude (default: Dornbirn)
    'lon': 9.7333             ##!< Seeker's longitude (default: Dornbirn)
}

def get_db_connection():
    """! Establish a connection to the MySQL database.
    @return mysql.connector.connection.MySQLConnection object if successful, None if failed
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# Utility function to calculate distance between two coordinates
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """! Calculate the great circle distance between two points on the earth.
    @param lat1 Latitude of the first point in decimal degrees
    @param lon1 Longitude of the first point in decimal degrees
    @param lat2 Latitude of the second point in decimal degrees
    @param lon2 Longitude of the second point in decimal degrees
    @return Distance in meters between the two points
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r * 1000  # Convert to meters


def bus_routes_get() -> List[Dict]:
    """! Get all available bus routes from the database.
    @return List of dictionaries containing route information 
            Each dictionary contains:
            - routeId: The unique identifier of the route
            - routeName: The name of the route
    @return ([{}], 500) on database error
    """
    conn = get_db_connection()
    if not conn:
        return [], 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM ro_routes")
        routes = cursor.fetchall()
        
        result = []
        for route in routes:
            route_obj = {
                "routeId": route['id'],
                "routeName": route['name']
            }
            result.append(route_obj)
        
        return result
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return [], 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def bus_stops_get() -> List[Dict]:
    """! Get all bus stops from the database.
    @return List of dictionaries containing bus stop information
            Each dictionary contains:
            - busStopId: The unique identifier of the bus stop
            - busStopName: The name of the bus stop
            - busStopLat: The latitude coordinate of the bus stop
            - busStopLon: The longitude coordinate of the bus stop
    @return ([{}], 500) on database error
    """
    conn = get_db_connection()
    if not conn:
        return [], 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, lat, lon FROM ro_stops")
        stops = cursor.fetchall()
        
        result = []
        for stop in stops:
            stop_obj = {
                "busStopId": stop['id'],
                "busStopName": stop['name'],
                "busStopLat": stop['lat'],
                "busStopLon": stop['lon']
            }
            result.append(stop_obj)
        
        return result
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return [], 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def bus_stops_in_range_get() -> List[Dict]:
    """! Get all bus stops within 400 meters of the seeker's current position.
    @return List of dictionaries containing nearby bus stop information
            Each dictionary contains:
            - busStopId: The unique identifier of the bus stop
            - busStopName: The name of the bus stop
            - busStopLat: The latitude coordinate of the bus stop
            - busStopLon: The longitude coordinate of the bus stop
    @note Uses SEEKER_INFO global variable for current seeker position
    @note Maximum range is 400 meters
    @return ([{}], 500) on database error
    """
    conn = get_db_connection()
    if not conn:
        return [], 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, lat, lon FROM ro_stops")
        stops = cursor.fetchall()
        
        result = []
        for stop in stops:
            # Calculate distance between seeker and this bus stop
            distance = haversine_distance(
                SEEKER_INFO['lat'], SEEKER_INFO['lon'],
                stop['lat'], stop['lon']
            )
            
            # Include stops within 400 meters
            if distance <= 400:
                stop_obj = {
                    "busStopId": stop['id'],
                    "busStopName": stop['name'],
                    "busStopLat": stop['lat'],
                    "busStopLon": stop['lon']
                }
                result.append(stop_obj)
        
        return result
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return [], 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def cards_card_id_discard_post(card_id: int) -> Tuple[None, int]:
    """! Discard a card from the player's hand.
    @param card_id The unique identifier of the card to discard
    @return (None, 200) if successful
    @return (None, 404) if card not found or not in hand
    @return (None, 500) on database error
    """
    conn = get_db_connection()
    if not conn:
        return None, 500
    
    try:
        cursor = conn.cursor()
        # Update card status to 'In Deck'
        cursor.execute(
            "UPDATE vtg_cards SET status = 'In Deck' WHERE id = %s AND status = 'In Hand'",
            (card_id,)
        )
        
        if cursor.rowcount == 0:
            return None, 404  # Card not found or not in hand
        
        conn.commit()
        return None, 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()
        return None, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def cards_card_id_use_post(card_id: int) -> Tuple[None, int]:
    """! Use a card from the player's hand.
    @param card_id The unique identifier of the card to use
    @return (None, 200) if successful
    @return (None, 404) if card not found or not in hand
    @return (None, 500) on database error
    @note For curse cards, they are added to the curses table with current timestamp
    @note Other cards are marked as 'In Effect'
    """
    conn = get_db_connection()
    if not conn:
        return None, 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        # First, check if the card exists and is in hand
        cursor.execute(
            """
            SELECT c.type FROM vtg_cards vc
            JOIN ro_cards c ON vc.card_id = c.id
            WHERE vc.id = %s AND vc.status = 'In Hand'
            """,
            (card_id,)
        )
        card = cursor.fetchone()
        
        if not card:
            return None, 404  # Card not found or not in hand
        
        # Update card status based on its type
        if card['type'] == 'curse':
            # For curse cards, add to curses table
            current_time = int(time.time())  # Unix timestamp
            cursor.execute(
                """
                UPDATE vtg_cards SET status = 'In Effect' WHERE id = %s;
                INSERT INTO vtg_curses (curse_id, asked_on)
                VALUES (%s, FROM_UNIXTIME(%s));
                """,
                (card_id, card_id, current_time)
            )
        else:
            # For other cards, just update status to 'In Effect'
            cursor.execute(
                "UPDATE vtg_cards SET status = 'In Effect' WHERE id = %s",
                (card_id,)
            )
        
        conn.commit()
        return None, 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()
        return None, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def cards_get() -> List[Dict]:
    """! Get all cards currently in the player's hand.
    @return List of dictionaries containing card information
            Each dictionary contains:
            - cardId: The unique identifier of the card
            - name: The name of the card
            - description: The description of the card's effect
            - type: The type of the card (e.g., 'curse')
    @return ([{}], 500) on database error
    """
    conn = get_db_connection()
    if not conn:
        return [], 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT vc.id as cardId, c.name, c.description, c.type
            FROM vtg_cards vc
            JOIN ro_cards c ON vc.card_id = c.id
            WHERE vc.status = 'In Hand'
            """
        )
        cards = cursor.fetchall()
        
        result = []
        for card in cards:
            card_obj = {
                "cardId": str(card['cardId']),
                "name": card['name'],
                "description": card['description'],
                "type": card['type']
            }
            result.append(card_obj)
        
        return result
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return [], 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def curses_curse_id_complete_post(curse_id: int) -> Tuple[None, int]:
    """! Mark a curse as completed and remove it from active curses.
    @param curse_id The unique identifier of the curse to complete
    @return (None, 200) if successful
    @return (None, 404) if curse not found
    @return (None, 500) on database error
    """
    conn = get_db_connection()
    if not conn:
        return None, 500
    
    try:
        cursor = conn.cursor()
        # Remove curse from active curses
        cursor.execute(
            "DELETE FROM vtg_curses WHERE id = %s",
            (curse_id,)
        )
        
        if cursor.rowcount == 0:
            return None, 404  # Curse not found
        
        # Update corresponding card status back to 'In Deck'
        cursor.execute(
            "UPDATE vtg_cards SET status = 'In Deck' WHERE id = %s",
            (curse_id,)
        )
        
        conn.commit()
        return None, 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()
        return None, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def curses_get() -> List[Dict]:
    """! Get all currently active curses.
    @return List of dictionaries containing curse information
            Each dictionary contains:
            - curseId: The unique identifier of the curse
            - name: The name of the curse
            - description: The description of the curse's effect
    @return ([{}], 500) on database error
    """
    conn = get_db_connection()
    if not conn:
        return [], 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.id as curseId, c.name, c.description
            FROM vtg_curses vc
            JOIN ro_cards c ON vc.curse_id = c.id
            """
        )
        curses = cursor.fetchall()
        
        result = []
        for curse in curses:
            curse_obj = {
                "curseId": str(curse['curseId']),
                "name": curse['name'],
                "description": curse['description']
            }
            result.append(curse_obj)
        
        return result
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return [], 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def exists_get() -> Tuple[None, int]:
    """! Check if the server is running and accessible.
    @return (None, 200) if server is running
    """
    return None, 200


def game_end_post() -> Tuple[None, int]:
    """! End the current game and reset all game state.
    @return (None, 200) if successful
    @return (None, 500) on database error
    @note Resets all temporary tables (cards, curses, questions)
    @note Resets global game state variables
    """
    global GAME_STATE
    
    GAME_STATE['is_started'] = False
    GAME_STATE['start_time'] = None
    
    conn = get_db_connection()
    if not conn:
        return None, 500
    
    try:
        cursor = conn.cursor()
        # Reset all temporary tables
        cursor.execute("TRUNCATE TABLE vtg_cards")
        cursor.execute("TRUNCATE TABLE vtg_curses")
        cursor.execute("TRUNCATE TABLE vtg_questions")
        
        conn.commit()
        return None, 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()
        return None, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def game_info_get() -> Dict:
    """! Get current game information.
    @return Dictionary containing game information:
            - currentGameTimer: Time elapsed since game start in seconds
            - hiderName: Name of the hider player
            - seekerName: Name of the seeker player
    """
    current_time = int(time.time())  # Current Unix timestamp
    current_game_timer = 0
    
    if GAME_STATE['is_started'] and GAME_STATE['start_time']:
        current_game_timer = current_time - GAME_STATE['start_time']
    
    game_info = {
        "currentGameTimer": current_game_timer,
        "hiderName": GAME_STATE['hider_name'],
        "seekerName": GAME_STATE['seeker_name']
    }
    
    return game_info


def game_start_post() -> Tuple[None, int]:
    """! Start a new game.
    @return (None, 200) if successful
    @return (None, 500) on database error
    @note Initializes card deck with all cards set to 'In Deck'
    @note Deals initial hand of 3 cards
    @note Initializes questions table with all questions set to 'Not Asked'
    @note Clears any existing curses
    """
    global GAME_STATE
    
    GAME_STATE['is_started'] = True
    GAME_STATE['start_time'] = int(time.time())  # Unix timestamp
    
    conn = get_db_connection()
    if not conn:
        return None, 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Initialize card deck - set all cards to 'In Deck'
        cursor.execute("SELECT id FROM ro_cards")
        cards = cursor.fetchall()
        
        # Clear existing cards
        cursor.execute("TRUNCATE TABLE vtg_cards")
        
        # Add all cards to deck
        for card in cards:
            cursor.execute(
                "INSERT INTO vtg_cards (card_id, status) VALUES (%s, 'In Deck')",
                (card['id'],)
            )
        
        # Deal initial hand (e.g., 3 cards)
        cursor.execute(
            """
            UPDATE vtg_cards
            SET status = 'In Hand'
            WHERE id IN (
                SELECT id FROM (
                    SELECT id FROM vtg_cards WHERE status = 'In Deck' LIMIT 3
                ) as temp
            )
            """
        )
        
        # Initialize questions
        cursor.execute("TRUNCATE TABLE vtg_questions")
        cursor.execute("SELECT id FROM ro_questions")
        questions = cursor.fetchall()
        
        for question in questions:
            cursor.execute(
                "INSERT INTO vtg_questions (question_id, status) VALUES (%s, 'Not Asked')",
                (question['id'],)
            )
        
        # Clear any existing curses
        cursor.execute("TRUNCATE TABLE vtg_curses")
        
        conn.commit()
        return None, 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()
        return None, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def game_swap_roles_post() -> Tuple[None, int]:
    """! Swap the roles of hider and seeker players.
    @return (None, 200) if successful
    @note Swaps player names in GAME_STATE
    @note Swaps player coordinates between HIDER_INFO and SEEKER_INFO
    @note Resets hider's bus_stop_id to None
    """
    global GAME_STATE, HIDER_INFO, SEEKER_INFO
    
    # Swap player names
    GAME_STATE['hider_name'], GAME_STATE['seeker_name'] = GAME_STATE['seeker_name'], GAME_STATE['hider_name']
    
    # Swap player coordinates
    hider_temp = HIDER_INFO.copy()
    HIDER_INFO['lat'] = SEEKER_INFO['lat']
    HIDER_INFO['lon'] = SEEKER_INFO['lon']
    HIDER_INFO['bus_stop_id'] = None  # Reset bus stop when swapping
    
    SEEKER_INFO['lat'] = hider_temp['lat']
    SEEKER_INFO['lon'] = hider_temp['lon']
    
    return None, 200


def hider_bus_stop_bus_stop_id_post(bus_stop_id: int) -> Tuple[None, int]:
    """! Set the bus stop where the hider is hiding.
    @param bus_stop_id The unique identifier of the chosen bus stop
    @return (None, 200) if successful
    @return (None, 404) if bus stop not found
    @return (None, 500) on database error
    @note Updates hider's coordinates to match the bus stop location
    """
    global HIDER_INFO
    
    conn = get_db_connection()
    if not conn:
        return None, 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, lat, lon FROM ro_stops WHERE id = %s",
            (bus_stop_id,)
        )
        bus_stop = cursor.fetchone()
        
        if not bus_stop:
            return None, 404  # Bus stop not found
        
        # Update hider's info
        HIDER_INFO['bus_stop_id'] = bus_stop_id
        HIDER_INFO['lat'] = bus_stop['lat']
        HIDER_INFO['lon'] = bus_stop['lon']
        
        return None, 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def hider_get_coordinates_get() -> Dict:
    """! Get the current coordinates of the hider.
    @return Dictionary containing hider's coordinates:
            - lat: Latitude coordinate
            - lon: Longitude coordinate
    """
    return {
        "lat": HIDER_INFO['lat'],
        "lon": HIDER_INFO['lon']
    }


def hider_info_get() -> Dict:
    """! Get detailed information about the hider's current location.
    @return Dictionary containing hider information:
            - lat: Latitude coordinate
            - lon: Longitude coordinate
            - busStationName: Name of the bus station (if at one)
            - busStationLat: Bus station latitude
            - busStationLon: Bus station longitude
            - busStationAltitude: Altitude of the bus station
            - busStationBezirk: District where the bus station is located
            - busStationGemeinde: Municipality where the bus station is located
            - distanceToNearestTrainStation: Distance to nearest train station
            - distanceToNearestMountain: Distance to nearest mountain
            - distanceToNearestMinigolf: Distance to nearest minigolf
            - distanceToNearestMuseum: Distance to nearest museum
    @return (Dict, 500) on database error with basic location info only
    """
    conn = get_db_connection()
    if not conn:
        return {}, 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        if not HIDER_INFO['bus_stop_id']:
            # Return basic info if no bus stop selected
            return {
                "lat": HIDER_INFO['lat'],
                "lon": HIDER_INFO['lon']
            }
        
        # Get bus stop details
        cursor.execute(
            """
            SELECT name, lat, lon, altitude, bezirk, gemeinde, 
                   distance_trainstation, distance_mountain, 
                   distance_minigolf, distance_museum
            FROM ro_stops
            WHERE id = %s
            """,
            (HIDER_INFO['bus_stop_id'],)
        )
        bus_stop = cursor.fetchone()
        
        if not bus_stop:
            return {}, 404
        
        hider_info = {
            "lat": HIDER_INFO['lat'],
            "lon": HIDER_INFO['lon'],
            "busStationName": bus_stop['name'],
            "busStationLat": bus_stop['lat'],
            "busStationLon": bus_stop['lon'],
            "busStationAltitude": bus_stop['altitude'],
            "busStationBezirk": bus_stop['bezirk'],
            "busStationGemeinde": bus_stop['gemeinde'],
            "distanceToNearestTrainStation": bus_stop['distance_trainstation'],
            "distanceToNearestMountain": bus_stop['distance_mountain'],
            "distanceToNearestMinigolf": bus_stop['distance_minigolf'],
            "distanceToNearestMuseum": bus_stop['distance_museum']
        }
        
        return hider_info
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return {}, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def hider_post_coordinates_post(body: Dict) -> Tuple[None, int]:
    """! Update the hider's coordinates.
    @param body Dictionary containing new coordinates:
                - lat: New latitude coordinate
                - lon: New longitude coordinate
    @return (None, 200) if successful
    @return (None, 400) if request body is invalid
    """
    global HIDER_INFO
    
    if connexion.request.is_json:
        data = connexion.request.get_json()
        
        # Update hider coordinates
        if 'lat' in data and 'lon' in data:
            HIDER_INFO['lat'] = data['lat']
            HIDER_INFO['lon'] = data['lon']
            return None, 200
    
    return None, 400  # Bad request


def questions_answer_post():
    """Answer current question"""
    conn = get_db_connection()
    if not conn:
        return None, 500
    
    try:
        cursor = conn.cursor()
        # Find the currently asked question
        cursor.execute(
            """
            UPDATE vtg_questions
            SET status = 'Previously Asked', answer = 'Answered'
            WHERE status = 'Currently Asked'
            """
        )
        
        if cursor.rowcount == 0:
            return None, 404  # No current question
        
        conn.commit()
        return None, 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()
        return None, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def questions_ask_question_id_post(question_id):
    """Ask a question"""
    conn = get_db_connection()
    if not conn:
        return None, 500
    
    try:
        cursor = conn.cursor()
        
        # First mark any current question as previously asked
        cursor.execute(
            """
            UPDATE vtg_questions
            SET status = 'Previously Asked', answer = 'Unanswered'
            WHERE status = 'Currently Asked'
            """
        )
        
        # Then set the new question as current with Unix timestamp
        current_time = int(time.time())
        cursor.execute(
            """
            UPDATE vtg_questions
            SET status = 'Currently Asked', asked_on = FROM_UNIXTIME(%s)
            WHERE question_id = %s AND status = 'Not Asked'
            """,
            (current_time, question_id)
        )
        
        if cursor.rowcount == 0:
            return None, 404  # Question not found or already asked
        
        conn.commit()
        return None, 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()
        return None, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def questions_current_get():
    """Get currently asked question info"""
    conn = get_db_connection()
    if not conn:
        return {}, 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT vq.id as questionId, q.name, q.description, 
                   UNIX_TIMESTAMP(vq.asked_on) as asked_on_unix,
                   q.time_minutes
            FROM vtg_questions vq
            JOIN ro_questions q ON vq.question_id = q.id
            WHERE vq.status = 'Currently Asked'
            """
        )
        question = cursor.fetchone()
        
        if not question:
            return {}, 404  # No current question
        
        # Calculate time left
        current_time = int(time.time())
        asked_on = question['asked_on_unix']
        time_limit_seconds = question['time_minutes'] * 60
        elapsed_seconds = current_time - asked_on
        time_left = max(0, time_limit_seconds - elapsed_seconds)
        
        return {
            "questionId": str(question['questionId']),
            "name": question['name'],
            "description": question['description'],
            "timeLeft": time_left
        }
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return {}, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def questions_get():
    """Get all questions"""
    conn = get_db_connection()
    if not conn:
        return [], 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT q.id, q.name, q.description, 
                   CASE WHEN vq.status != 'Not Asked' THEN 1 ELSE 0 END as already_asked
            FROM ro_questions q
            JOIN vtg_questions vq ON q.id = vq.question_id
            """
        )
        questions = cursor.fetchall()
        
        result = []
        for question in questions:
            question_obj = {
                "id": str(question['id']),
                "name": question['name'],
                "description": question['description'],
                "alreadyAsked": bool(question['already_asked'])
            }
            result.append(question_obj)
        
        return result
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return [], 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def questions_previous_get():
    """Get previously asked questions info"""
    conn = get_db_connection()
    if not conn:
        return [], 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT vq.id as questionId, q.name, q.description, vq.answer
            FROM vtg_questions vq
            JOIN ro_questions q ON vq.question_id = q.id
            WHERE vq.status = 'Previously Asked'
            ORDER BY vq.asked_on DESC
            """
        )
        questions = cursor.fetchall()
        
        result = []
        for question in questions:
            question_obj = {
                "questionId": str(question['questionId']),
                "name": question['name'],
                "description": question['description'],
                "answer": question['answer'] if question['answer'] else "No answer"
            }
            result.append(question_obj)
        
        return result
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return [], 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def questions_veto_post():
    """Veto current question"""
    conn = get_db_connection()
    if not conn:
        return None, 500
    
    try:
        cursor = conn.cursor()
        
        # Find and update the current question
        cursor.execute(
            """
            UPDATE vtg_questions
            SET status = 'Not Asked', asked_on = NULL
            WHERE status = 'Currently Asked'
            """
        )
        
        if cursor.rowcount == 0:
            return None, 404  # No current question
        
        conn.commit()
        return None, 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()
        return None, 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def seeker_get_coordinates_get() -> Dict:
    """! Get the current coordinates of the seeker.
    @return Dictionary containing seeker's coordinates:
            - lat: Latitude coordinate
            - lon: Longitude coordinate
    """
    return {
        "lat": SEEKER_INFO['lat'],
        "lon": SEEKER_INFO['lon']
    }


def seeker_info_get() -> Dict:
    """! Get detailed information about the seeker's current location.
    @return Dictionary containing seeker information:
            - lat: Latitude coordinate
            - lon: Longitude coordinate
            - altitude: Current altitude
            - bezirk: Current district
            - gemeinde: Current municipality
            - distanceToNearestTrainStation: Distance to nearest train station
            - distanceToNearestMountain: Distance to nearest mountain
            - distanceToNearestMinigolf: Distance to nearest minigolf
            - distanceToNearestMuseum: Distance to nearest museum
    @return Basic info dict with default values on database error
    """
    conn = get_db_connection()
    if not conn:
        return {}, 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get the administrative region and POI distances for seeker's location
        # Find the administrative region (bezirk and gemeinde)
        cursor.execute(
            """
            SELECT bezirk, gemeinde
            FROM ro_boundaries
            WHERE ST_Contains(
                shape_data,
                POINT(%s, %s)
            )
            """,
            (SEEKER_INFO['lon'], SEEKER_INFO['lat'])
        )
        region = cursor.fetchone()
        
        # Find altitude and distances to POIs
        cursor.execute(
            """
            SELECT 
                (SELECT altitude FROM ro_stops ORDER BY 
                    ST_Distance_Sphere(POINT(lon, lat), POINT(%s, %s)) LIMIT 1) as altitude,
                (SELECT ST_Distance_Sphere(POINT(lon, lat), POINT(%s, %s)) 
                    FROM ro_points_of_interest WHERE type = 'train_station' 
                    ORDER BY ST_Distance_Sphere(POINT(lon, lat), POINT(%s, %s)) LIMIT 1) as dist_train,
                (SELECT ST_Distance_Sphere(POINT(lon, lat), POINT(%s, %s)) 
                    FROM ro_points_of_interest WHERE type = 'mountain' 
                    ORDER BY ST_Distance_Sphere(POINT(lon, lat), POINT(%s, %s)) LIMIT 1) as dist_mountain,
                (SELECT ST_Distance_Sphere(POINT(lon, lat), POINT(%s, %s)) 
                    FROM ro_points_of_interest WHERE type = 'minigolf' 
                    ORDER BY ST_Distance_Sphere(POINT(lon, lat), POINT(%s, %s)) LIMIT 1) as dist_minigolf,
                (SELECT ST_Distance_Sphere(POINT(lon, lat), POINT(%s, %s)) 
                    FROM ro_points_of_interest WHERE type = 'museum' 
                    ORDER BY ST_Distance_Sphere(POINT(lon, lat), POINT(%s, %s)) LIMIT 1) as dist_museum
            """,
            (SEEKER_INFO['lon'], SEEKER_INFO['lat'],
             SEEKER_INFO['lon'], SEEKER_INFO['lat'], SEEKER_INFO['lon'], SEEKER_INFO['lat'],
             SEEKER_INFO['lon'], SEEKER_INFO['lat'], SEEKER_INFO['lon'], SEEKER_INFO['lat'],
             SEEKER_INFO['lon'], SEEKER_INFO['lat'], SEEKER_INFO['lon'], SEEKER_INFO['lat'],
             SEEKER_INFO['lon'], SEEKER_INFO['lat'], SEEKER_INFO['lon'], SEEKER_INFO['lat'])
        )
        poi_data = cursor.fetchone()
        
        # Prepare seeker info
        seeker_info = {
            "lat": SEEKER_INFO['lat'],
            "lon": SEEKER_INFO['lon'],
            "altitude": poi_data['altitude'] if poi_data and poi_data['altitude'] else 0,
            "bezirk": region['bezirk'] if region else "Unknown",
            "gemeinde": region['gemeinde'] if region else "Unknown",
            "distanceToNearestTrainStation": poi_data['dist_train'] if poi_data and poi_data['dist_train'] else 0,
            "distanceToNearestMountain": poi_data['dist_mountain'] if poi_data and poi_data['dist_mountain'] else 0,
            "distanceToNearestMinigolf": poi_data['dist_minigolf'] if poi_data and poi_data['dist_minigolf'] else 0,
            "distanceToNearestMuseum": poi_data['dist_museum'] if poi_data and poi_data['dist_museum'] else 0
        }
        
        return seeker_info
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        # Return basic info if database query fails
        return {
            "lat": SEEKER_INFO['lat'],
            "lon": SEEKER_INFO['lon'],
            "altitude": 0,
            "bezirk": "Unknown",
            "gemeinde": "Unknown",
            "distanceToNearestTrainStation": 0,
            "distanceToNearestMountain": 0,
            "distanceToNearestMinigolf": 0,
            "distanceToNearestMuseum": 0
        }
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def seeker_post_coordinates_post(body):
    """Post coordinates of seeker"""
    global SEEKER_INFO
    
    if connexion.request.is_json:
        data = connexion.request.get_json()
        
        # Update seeker coordinates
        if 'lat' in data and 'lon' in data:
            SEEKER_INFO['lat'] = data['lat']
            SEEKER_INFO['lon'] = data['lon']
            
            # Check if seeker is within capture range of hider
            if HIDER_INFO['bus_stop_id']:
                distance = haversine_distance(
                    SEEKER_INFO['lat'], SEEKER_INFO['lon'],
                    HIDER_INFO['lat'], HIDER_INFO['lon']
                )
                
                # If seeker is within 20 meters of hider, game is over
                if distance <= 20:
                    # We could trigger game end logic here
                    pass
            
            return None, 200
    
    return None, 400  # Bad request
