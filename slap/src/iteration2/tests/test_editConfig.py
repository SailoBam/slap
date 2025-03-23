from services.slapStore import SlapStore, Config


def test_editConfig_updates_existing_config(self):
        """Test that editConfig updates an existing config"""
        print("--------------------------------")
        print("")
        print("UNIT TEST: Config_Edit")
        print("\nTesting editing of existing config...")
        
        # Create initial config
        initial_config = Config(0, "Test Config", 1, 2, 3)
        initial_config = self.store.newConfig(initial_config)
        
        # Edit the config
        edited_config = Config(initial_config.configId, "Edited Config", 10, 20, 30)
        self.store.updateConfig(edited_config)
        
        # Verify config was updated in database
        self.store.cursor.execute(f"SELECT * FROM CONFIGS WHERE configId = '{initial_config.configId}'")
        saved_config = self.store.cursor.fetchone()
        self.assertIsNotNone(saved_config)
        
        print("Verifying saved values match edited values...")
        self.assertEqual(saved_config['name'], 'Edited Config')
        self.assertEqual(saved_config['proportional'], 10)
        self.assertEqual(saved_config['integral'], 20)
        self.assertEqual(saved_config['differential'], 30)
        print("All values verified successfully")
