import unittest
import os
import sqlite3
from src.iteration2.services.slapStore import SlapStore, Config

class TestSlapStore(unittest.TestCase):
    def setUp(self):
        """Set up a test database before each test"""
        self.test_db = "test_slap.db"
        self.store = SlapStore()
        # Store original database name
        self.original_db = self.store.connection.get_info(sqlite3.SQLITE_DATABASE_NAME)
        # Close original connection
        self.store.connection.close()
        # Create new connection to test database
        self.store.connection = sqlite3.connect(self.test_db, check_same_thread=False)
        self.store.connection.row_factory = sqlite3.Row
        self.store.cursor = self.store.connection.cursor()
        # Create tables
        self.store.cursor.execute('''
            CREATE TABLE IF NOT EXISTS CONFIGS (
                configId INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                proportional REAL NOT NULL,
                integral REAL NOT NULL,
                differential REAL NOT NULL,
                isDefault BOOLEAN
            )
        ''')
        self.store.connection.commit()

    def tearDown(self):
        """Clean up after each test"""
        self.store.connection.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_getCurrentConfig_creates_default_when_none_exists(self):
        """Test that getCurrentConfig creates a default config when none exists"""
        # Get current config (should create default)
        config = self.store.getCurrentConfig()
        
        # Verify default config was created
        self.assertEqual(config.name, 'Default')
        self.assertEqual(config.proportional, 0)
        self.assertEqual(config.integral, 0)
        self.assertEqual(config.differential, 0)
        
        # Verify config was saved to database
        self.store.cursor.execute("SELECT * FROM CONFIGS WHERE isDefault = True")
        saved_config = self.store.cursor.fetchone()
        self.assertIsNotNone(saved_config)
        self.assertEqual(saved_config['name'], 'Default')
        self.assertEqual(saved_config['proportional'], 0)
        self.assertEqual(saved_config['integral'], 0)
        self.assertEqual(saved_config['differential'], 0)

if __name__ == '__main__':
    unittest.main() 