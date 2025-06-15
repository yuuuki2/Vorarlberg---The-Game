import unittest
import mysql.connector
import sys
from datetime import datetime

# Connection parameters for vtg_server user
VTG_CONFIG = {
    'user': 'vtg_server',
    'password': 'vtg_server',
    'host': 'localhost',
    'database': 'vtg_data'
}

class TestVTGServerPermissions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Connect to the database before running tests"""
        try:
            cls.conn = mysql.connector.connect(**VTG_CONFIG)
            cls.cursor = cls.conn.cursor()
            print("Connected to database as vtg_server")
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
            sys.exit(1)
    
    @classmethod
    def tearDownClass(cls):
        """Close database connection after all tests"""
        if hasattr(cls, 'conn') and cls.conn.is_connected():
            cls.conn.close()
            print("Database connection closed.")
    
    def test_01_insert_data(self):
        """Test if vtg_server can insert data into vtg_cards table"""
        print("\nTest 1: Inserting data into vtg_cards...")
        try:
            # First check if table exists
            self.cursor.execute("SHOW TABLES LIKE 'vtg_cards'")
            if not self.cursor.fetchone():
                self.skipTest("vtg_cards table does not exist")
                
            # Find a valid card_id to use
            self.cursor.execute("SELECT id FROM ro_cards LIMIT 1")
            card_id_result = self.cursor.fetchone()
            if not card_id_result:
                self.skipTest("No cards found in ro_cards table")
                
            card_id = card_id_result[0]
            
            # Insert a new card record
            self.cursor.execute(
                "INSERT INTO vtg_cards (card_id, status) VALUES (%s, %s)", 
                (card_id, "In Deck")
            )
            self.conn.commit()
            self.assertTrue(True, "Data inserted successfully into vtg_cards")
        except mysql.connector.Error as err:
            self.fail(f"Failed to insert data: {err}")
    
    def test_02_update_data(self):
        """Test if vtg_server can update data in vtg_cards table"""
        print("\nTest 2: Updating data in vtg_cards...")
        try:
            # First check if table exists
            self.cursor.execute("SHOW TABLES LIKE 'vtg_cards'")
            if not self.cursor.fetchone():
                self.skipTest("vtg_cards table does not exist")
                
            # Find a card record to update
            self.cursor.execute("SELECT id FROM vtg_cards WHERE status = 'In Deck' LIMIT 1")
            card_result = self.cursor.fetchone()
            if not card_result:
                self.skipTest("No suitable cards found to update")
                
            card_record_id = card_result[0]
            
            # Update the card status
            self.cursor.execute(
                "UPDATE vtg_cards SET status = %s WHERE id = %s", 
                ("In Hand", card_record_id)
            )
            self.conn.commit()
            self.assertTrue(True, "Data updated successfully in vtg_cards")
        except mysql.connector.Error as err:
            self.fail(f"Failed to update data: {err}")
    
    def test_03_delete_data(self):
        """Test if vtg_server can delete data from vtg_cards table"""
        print("\nTest 3: Deleting data from vtg_cards...")
        try:
            # First check if table exists
            self.cursor.execute("SHOW TABLES LIKE 'vtg_cards'")
            if not self.cursor.fetchone():
                self.skipTest("vtg_cards table does not exist")
                
            # Find a card record to delete
            self.cursor.execute("SELECT id FROM vtg_cards WHERE status = 'In Hand' LIMIT 1")
            card_result = self.cursor.fetchone()
            if not card_result:
                self.skipTest("No suitable cards found to delete")
                
            card_record_id = card_result[0]
            
            # Delete the card record
            self.cursor.execute("DELETE FROM vtg_cards WHERE id = %s", (card_record_id,))
            self.conn.commit()
            self.assertTrue(True, "Data deleted successfully from vtg_cards")
        except mysql.connector.Error as err:
            self.fail(f"Failed to delete data: {err}")
    
    def test_04_insert_curse(self):
        """Test if vtg_server can insert data into vtg_curses table"""
        print("\nTest 4: Inserting data into vtg_curses...")
        try:
            # First check if table exists
            self.cursor.execute("SHOW TABLES LIKE 'vtg_curses'")
            if not self.cursor.fetchone():
                self.skipTest("vtg_curses table does not exist")
                
            # Find a valid curse_id to use
            self.cursor.execute("SELECT id FROM ro_cards WHERE type = 'curse' LIMIT 1")
            curse_id_result = self.cursor.fetchone()
            if not curse_id_result:
                self.skipTest("No curse cards found in ro_cards table")
                
            curse_id = curse_id_result[0]
            current_time = datetime.now()
            
            # Insert a new curse record
            self.cursor.execute(
                "INSERT INTO vtg_curses (curse_id, asked_on) VALUES (%s, %s)", 
                (curse_id, current_time)
            )
            self.conn.commit()
            self.assertTrue(True, "Data inserted successfully into vtg_curses")
        except mysql.connector.Error as err:
            self.fail(f"Failed to insert curse: {err}")
    
    def test_05_insert_question(self):
        """Test if vtg_server can insert data into vtg_questions table"""
        print("\nTest 5: Inserting data into vtg_questions...")
        try:
            # First check if table exists
            self.cursor.execute("SHOW TABLES LIKE 'vtg_questions'")
            if not self.cursor.fetchone():
                self.skipTest("vtg_questions table does not exist")
                
            # Find a valid question_id to use
            self.cursor.execute("SELECT id FROM ro_questions LIMIT 1")
            question_id_result = self.cursor.fetchone()
            if not question_id_result:
                self.skipTest("No questions found in ro_questions table")
                
            question_id = question_id_result[0]
            
            # Insert a new question record
            self.cursor.execute(
                "INSERT INTO vtg_questions (question_id, status, answer, asked_on) VALUES (%s, %s, %s, %s)", 
                (question_id, "Not Asked", None, None)
            )
            self.conn.commit()
            self.assertTrue(True, "Data inserted successfully into vtg_questions")
        except mysql.connector.Error as err:
            self.fail(f"Failed to insert question: {err}")
    
    def test_06_read_ro_table(self):
        """Test if vtg_server can read from a ro_table"""
        print("\nTest 6: Reading from ro_stops...")
        try:
            # First check if the table exists
            self.cursor.execute("SHOW TABLES LIKE 'ro_stops'")
            if self.cursor.fetchone():
                self.cursor.execute("SELECT * FROM ro_stops LIMIT 5")
                rows = self.cursor.fetchall()
                self.assertTrue(len(rows) > 0, "Successfully read rows from ro_stops")
            else:
                self.skipTest("ro_stops table does not exist")
        except mysql.connector.Error as err:
            self.fail(f"Failed to read from ro_stops: {err}")
    
    def test_07_modify_ro_table(self):
        """Test if vtg_server cannot modify a ro_table (should fail)"""
        print("\nTest 7: Attempting to modify ro_table (should fail)...")
        with self.assertRaises(mysql.connector.Error):
            self.cursor.execute("UPDATE ro_stops SET name = 'test' WHERE id = (SELECT id FROM ro_stops LIMIT 1)")
            self.conn.commit()
    
    def test_08_drop_ro_table(self):
        """Test if vtg_server cannot drop a ro_table (should fail)"""
        print("\nTest 8: Attempting to drop ro_table (should fail)...")
        with self.assertRaises(mysql.connector.Error):
            self.cursor.execute("DROP TABLE ro_stops")
            self.conn.commit()

if __name__ == "__main__":
    print("Testing vtg_server user permissions...")
    unittest.main(verbosity=2)