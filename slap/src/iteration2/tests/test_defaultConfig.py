def test_getCurrentConfig_creates_default_when_none_exists(self):
        """Test that getCurrentConfig creates a default config when none exists"""
        print("--------------------------------")
        print("")
        print("UNIT TEST: Config_Default")
        print("\nTesting creation of default config...")
        
        # Get current config (should create default)
        config = self.store.getCurrentConfig()
        
        # Verify default config was created
        self.assertEqual(config.name, 'Default')
        
        # Verify config was saved to database
        self.store.cursor.execute("SELECT * FROM CONFIGS WHERE isDefault = True")
        saved_config = self.store.cursor.fetchone()
        self.assertIsNotNone(saved_config)
        
        print("Verifying saved values match default values...")
        self.assertEqual(saved_config['name'], 'Default')
        self.assertEqual(saved_config['proportional'], 0)
        self.assertEqual(saved_config['integral'], 0)
        self.assertEqual(saved_config['differential'], 0)
        print("All values verified successfully")
