import unittest
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import and run the tests
from tests.tests import Test

if __name__ == '__main__':
    unittest.main() 