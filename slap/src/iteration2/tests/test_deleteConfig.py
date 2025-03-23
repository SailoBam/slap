from services.slapStore import SlapStore, Config


def test_deleteConfig_removes_existing_config(self):
        """Test that deleteConfig removes an existing config"""
        print("--------------------------------")
        print("")
        print("UNIT TEST: Config_Delete") 
        print("\nTesting deletion of existing config...")
        
        # Create initial config
        initial_config = Config(0, "Test Config", 1, 2, 3)
        initial_config = self.store.newConfig(initial_config)
        
        # Delete the config
        self.store.deleteConfig(initial_config.configId)
        
        # Verify config was deleted from database
        self.store.cursor.execute(f"SELECT * FROM CONFIGS WHERE configId = '{initial_config.configId}'")
        deleted_config = self.store.cursor.fetchone()
        
        print("Verifying config was deleted...")
        self.assertIsNone(deleted_config)
        print("Config deletion verified successfully")
