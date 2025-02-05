
import unittest
from slapStore import SlapStore, Boat

class SlapStoreTest(unittest.TestCase):

    def setUp(self):
        global slapStore
        slapStore = SlapStore()

    def test_addBoat(self):
        boat = Boat(model = "tiki 26", name = "frygga", id = 0)

        slapStore.addBoat(boat)
        row = slapStore.getBoat('frygga')
        print(row)
        self.assertEqual(row[1], 'frygga')
        self.assertEqual(row[2], 'tiki 26')
        
    
if __name__ == '__main__':
    unittest.main()