#Prompt 1: Based on the concepts in concept.md and databases.md, the login data and db scheme from create_db.py, create a python program that creates all the permanent databases outlined in databases.md
# Prompt 2: Based on the information in questions.md, populate the questions table with the questions from questions.md
# Prompt 3: Based on the information in cards_and_curses.md, populate the cards table with the cards from cards_and_curses.md. For the curses, use the description "Besuche https://jetlag.collinj.dev/cards für weitere Informationen".

import mysql.connector
import sys

# MariaDB connection parameters
DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'vtg_data'
}

def init_db():
    """Initialize the database and create the card and question tables"""
    try:
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
        
        # Create card data table (RO_Carddata)
        print("Creating card data table...")
        c.execute("""
        CREATE TABLE IF NOT EXISTS ro_cards (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            type ENUM('time_bonus', 'curse', 'power_up') NOT NULL
        ) ENGINE=InnoDB
        """)
        
        # Create question data table (RO_Questiondata)
        print("Creating question data table...")
        c.execute("""
        CREATE TABLE IF NOT EXISTS ro_questions (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            type ENUM('comparing', 'measuring', 'thermometer', 'radar', 'photo') NOT NULL,
            time_minutes INT NOT NULL,
            num_cards_to_choose INT NOT NULL
        ) ENGINE=InnoDB
        """)
        
        # Create card tracking table (vtg_cards)
        print("Creating card tracking table...")
        c.execute("""
        CREATE TABLE IF NOT EXISTS vtg_cards (
            id INT PRIMARY KEY AUTO_INCREMENT,
            card_id INT NOT NULL,
            status ENUM('In Hand', 'In Deck', 'In Effect') NOT NULL,
            FOREIGN KEY (card_id) REFERENCES ro_cards(id)
        ) ENGINE=InnoDB
        """)
        
        # Create curse tracking table (vtg_curses)
        print("Creating curse tracking table...")
        c.execute("""
        CREATE TABLE IF NOT EXISTS vtg_curses (
            id INT PRIMARY KEY AUTO_INCREMENT,
            curse_id INT NOT NULL,
            asked_on DATETIME NOT NULL,
            FOREIGN KEY (curse_id) REFERENCES ro_cards(id)
        ) ENGINE=InnoDB
        """)
        
        # Create question tracking table (vtg_questions)
        print("Creating question tracking table...")
        c.execute("""
        CREATE TABLE IF NOT EXISTS vtg_questions (
            id INT PRIMARY KEY AUTO_INCREMENT,
            question_id INT NOT NULL,
            status ENUM('Not Asked', 'Currently Asked', 'Previously Asked') NOT NULL,
            answer TEXT,
            asked_on DATETIME,
            FOREIGN KEY (question_id) REFERENCES ro_questions(id)
        ) ENGINE=InnoDB
        """)
        
        conn.commit()
        print("All tables created successfully!")
        
        return conn
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)

def populate_questions(conn):
    """Populate the questions table with data from questions.md"""
    c = conn.cursor()
    
    # Clear existing questions to avoid duplicates
    c.execute("DELETE FROM ro_questions")
    print("Cleared existing questions. Adding new questions...")
    
    # Comparing questions (Draw 3, Pick 1)
    comparing_questions = [
        ("Bushaltestellen-Vergleich", "Hält mein Bus auch an deinem Standort?", "comparing", 5, 3),
        ("Länge des Haltestellennamens", "Hat deine Bushaltestelle die gleiche Anzahl an Buchstaben wie meine?", "comparing", 5, 3),
        ("Gleiche Straße", "Befindest du dich auf der gleichen Straße/dem gleichen Weg wie ich? (Falls ich nicht auf einer Straße bin, wird die nächstgelegene verwendet)", "comparing", 5, 3),
        ("Gleicher Bezirk", "Bist du im gleichen Bezirk wie ich?", "comparing", 5, 3),
        ("Gleiche Gemeinde", "Bist du in der gleichen Gemeinde wie ich?", "comparing", 5, 3)
    ]
    
    # Measuring questions (Draw 3, Pick 1)
    measuring_questions = [
        ("Entfernung zum Bahnhof", "Wie weit ist es zum nächsten Bahnhof? (gerundet auf 2 Kilometer)", "measuring", 5, 3),
        ("Entfernung zum Berg", "Wie weit ist es zum nächsten Berg? (gerundet auf 2 Kilometer)", "measuring", 5, 3),
        ("Entfernung zum Minigolfplatz", "Wie weit ist es zum nächsten Minigolfplatz? (gerundet auf 2 Kilometer)", "measuring", 5, 3),
        ("Entfernung zum Museum", "Wie weit ist es zum nächsten Museum? (gerundet auf 2 Kilometer)", "measuring", 5, 3)
    ]
    
    # Radar questions (Draw 2, Pick 1)
    radar_questions = [
        ("500m Radar", "Befindest du dich innerhalb von 500m zu den Suchenden?", "radar", 5, 2),
        ("1km Radar", "Befindest du dich innerhalb von 1km zu den Suchenden?", "radar", 5, 2),
        ("2km Radar", "Befindest du dich innerhalb von 2km zu den Suchenden?", "radar", 5, 2),
        ("5km Radar", "Befindest du dich innerhalb von 5km zu den Suchenden?", "radar", 5, 2),
        ("8km Radar", "Befindest du dich innerhalb von 8km zu den Suchenden?", "radar", 5, 2),
        ("15km Radar", "Befindest du dich innerhalb von 15km zu den Suchenden?", "radar", 5, 2),
        ("40km Radar", "Befindest du dich innerhalb von 40km zu den Suchenden?", "radar", 5, 2),
        ("Benutzerdefiniertes Radar", "Befindest du dich innerhalb einer selbst gewählten Entfernung zu den Suchenden?", "radar", 5, 2)
    ]
    
    # Thermometer questions (Draw 2, Pick 1)
    thermometer_questions = [
        ("750m Thermometer", "Die Suchenden bewegen sich 750m. Sind sie jetzt näher bei dir oder weiter weg?", "thermometer", 5, 2),
        ("5km Thermometer", "Die Suchenden bewegen sich 5km. Sind sie jetzt näher bei dir oder weiter weg?", "thermometer", 5, 2),
        ("15km Thermometer", "Die Suchenden bewegen sich 15km. Sind sie jetzt näher bei dir oder weiter weg?", "thermometer", 5, 2)
    ]
    
    # Photo questions (Draw 1, Pick 1)
    photo_questions = [
        ("Baum-Foto", "Mache ein Foto von einem Baum (der gesamte Baum muss zu sehen sein)", "photo", 10, 1),
        ("Himmel-Foto", "Mache ein Foto vom Himmel (Lege das Handy auf den Boden und fotografiere direkt nach oben)", "photo", 10, 1),
        ("Selfie", "Mache ein Selfie (Arm vollständig ausgestreckt, parallel zum Boden)", "photo", 10, 1),
        ("Höchstes Bauwerk", "Fotografiere das höchste von Menschen geschaffene Bauwerk (das von deinem Standort aus am höchsten erscheint. Muss die Spitze und zwei Seiten der Struktur zeigen. Ein Bauwerk kann ein Gebäude sein, aber auch ein Strommast, ein TV-Sendemast, usw.)", "photo", 10, 1),
        ("Sichtbares Gebäude", "Fotografiere ein von deiner Bushaltestelle aus sichtbares Gebäude (Kann ein beliebiges Gebäude sein. Muss die Spitze und zwei Seiten des Gebäudes zeigen)", "photo", 10, 1),
        ("Gebäude vom Bahnhof", "Fotografiere das höchste von Menschen geschaffene Gebäude vom Bahnhof aus (das von deinem Standort aus am höchsten erscheint. Muss die Spitze und zwei Seiten der Struktur zeigen)", "photo", 10, 1),
        ("Zwei Gebäude", "Fotografiere zwei Gebäude (Muss einen Bereich von 1,5×1,5 Metern mit 3 unterschiedlichen Elementen enthalten)", "photo", 10, 1),
        ("Bushaltestelle", "Fotografiere eine Bushaltestelle (Muss einen Bereich von 1,5×1,5 Metern mit 3 unterschiedlichen Elementen enthalten)", "photo", 10, 1),
        ("Religiöses Gebäude", "Fotografiere einen Ort der Andacht (Kirche, Moschee, Bildstock, Marienschrein, Kapelle, usw.)", "photo", 10, 1),
        ("Höchster Berg", "Fotografiere den höchsten Berg (der von deinem Standort aus am höchsten erscheint. Nicht der tatsächlich höchste in Bezug auf die Meereshöhe)", "photo", 10, 1)
    ]
    
    # Combine all questions
    all_questions = comparing_questions + measuring_questions + radar_questions + thermometer_questions + photo_questions
    
    # Insert all questions into the database
    insert_query = """
    INSERT INTO ro_questions (name, description, type, time_minutes, num_cards_to_choose)
    VALUES (%s, %s, %s, %s, %s)
    """
    c.executemany(insert_query, all_questions)
    conn.commit()
    
    print(f"Added {len(all_questions)} questions to the database")

def populate_cards(conn):
    """Populate the cards table with data from cards_and_curses.md"""
    c = conn.cursor()
    
    # Clear existing cards to avoid duplicates
    c.execute("DELETE FROM ro_cards")
    print("Cleared existing cards. Adding new cards...")
    
    # Time Bonus cards
    time_bonus_cards = [
        ("3 Minuten Zeitbonus", "Gibt dem Verstecker 3 zusätzliche Minuten Zeit.", "time_bonus"),
        ("6 Minuten Zeitbonus", "Gibt dem Verstecker 6 zusätzliche Minuten Zeit.", "time_bonus"),
        ("10 Minuten Zeitbonus", "Gibt dem Verstecker 10 zusätzliche Minuten Zeit.", "time_bonus"),
        ("15 Minuten Zeitbonus", "Gibt dem Verstecker 15 zusätzliche Minuten Zeit.", "time_bonus"),
        ("20 Minuten Zeitbonus", "Gibt dem Verstecker 20 zusätzliche Minuten Zeit.", "time_bonus")
    ]
    
    # Power Up cards
    power_up_cards = [
        ("Zufallskarte", "Wenn die Suchenden eine Frage stellen, kannst du sie zufällig durch eine andere ersetzen. Du erhältst die Belohnungskarten dieser Frage.", "power_up"),
        ("Veto", "Wenn die Suchenden eine Frage stellen, kannst du dich weigern, sie zu beantworten. Du erhältst trotzdem die mit dieser Frage verbundenen Belohnungskarten.", "power_up"),
        ("Duplizieren", "Du kannst eine andere Karte duplizieren.", "power_up"),
        ("Umziehen", "Du kannst deinen Versteckplatz wechseln. Die Suchenden sehen deinen alten Versteckplatz, können sich aber 30 Minuten lang nicht bewegen. In diesen 30 Minuten kannst du zu einem neuen Versteckplatz gelangen.", "power_up"),
        ("1 Abwerfen, 2 Ziehen", "Wirf 1 Karte aus deinem Deck ab und ziehe 2 neue.", "power_up"),
        ("2 Abwerfen, 3 Ziehen", "Wirf 2 Karten aus deinem Deck ab und ziehe 3 neue.", "power_up")
    ]
    
    # Curse cards - all with the same description as requested
    curse_description = "Besuche https://jetlag.collinj.dev/cards für weitere Informationen"
    curse_cards = [
        ("Fluch des Zoologen", curse_description, "curse"),
        ("Fluch des orientierungslosen Touristen", curse_description, "curse"),
        ("Fluch des endlosen Sturzes", curse_description, "curse"),
        ("Fluch des versteckten Henkers", curse_description, "curse"),
        ("Fluch des überlaufenden Kelchs", curse_description, "curse"),
        ("Fluch des mittelmäßigen Reiseagenten", curse_description, "curse"),
        ("Fluch des Luxusautos", curse_description, "curse"),
        ("Fluch der Kehrtwende", curse_description, "curse"),
        ("Fluch des Brückentrolls", curse_description, "curse"),
        ("Fluch des Wassergewichts", curse_description, "curse"),
        ("Fluch der verklemmten Tür", curse_description, "curse"),
        ("Fluch des Steinmännchens", curse_description, "curse"),
        ("Fluch des Stadtentdeckers", curse_description, "curse"),
        ("Fluch des beeinflussbaren Konsumenten", curse_description, "curse"),
        ("Fluch des Ei-Partners", curse_description, "curse"),
        ("Fluch der fernen Küche", curse_description, "curse"),
        ("Fluch der Rechtskurve", curse_description, "curse"),
        ("Fluch des Labyrinths", curse_description, "curse"),
        ("Fluch des Vogelführers", curse_description, "curse"),
        ("Fluch des fleckigen Gedächtnisses", curse_description, "curse"),
        ("Fluch des Zitronen-Phylakteriums", curse_description, "curse"),
        ("Fluch des erschöpften Gehirns", curse_description, "curse"),
        ("Fluch der Lösegeldforderung", curse_description, "curse"),
        ("Fluch der Spielerfüße", curse_description, "curse")
    ]
    
    # Combine all cards
    all_cards = time_bonus_cards + power_up_cards + curse_cards
    
    # Insert all cards into the database
    insert_query = """
    INSERT INTO ro_cards (name, description, type)
    VALUES (%s, %s, %s)
    """
    c.executemany(insert_query, all_cards)
    conn.commit()
    
    print(f"Added {len(all_cards)} cards to the database")

def main():
    print("Creating card and question tables for Vorarlberg - The Game...")
    conn = init_db()
    
    try:
        # Populate the questions table
        populate_questions(conn)
        
        # Populate the cards table
        populate_cards(conn)
        
        print("Tables creation and population complete!")
    except mysql.connector.Error as err:
        print(f"Error populating tables: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()