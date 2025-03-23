from services.slapStore import SlapStore, Config

def test_createConfig_creates_new_config(self):
        """Test that createConfig creates a config"""
        print("--------------------------------")
        print("")
        print("UNIT TEST: Config_Create")
        print("\nTesting creation of new config...")
        
        # Get current config (should create default)
        config = Config(0, "My Custom Config", 10, 5, 1)
 
        config = self.store.newConfig(config)

        self.assertEqual(config.name, 'My Custom Config')
        
        # Verify config was saved to database
        self.store.cursor.execute(f"SELECT * FROM CONFIGS WHERE configId = '{config.configId}'")
        saved_config = self.store.cursor.fetchone()
        self.assertIsNotNone(saved_config)
        
        print("Verifying saved values match input values...")
        self.assertEqual(saved_config['name'], 'My Custom Config')
        self.assertEqual(saved_config['proportional'], 10)
        self.assertEqual(saved_config['integral'], 5)
        self.assertEqual(saved_config['differential'], 1)
        print("All values verified successfully")