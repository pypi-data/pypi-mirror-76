
import unittest
import sys
from pyvisionproductsearch.Vision import *
from random import randint
import os

LOCATION = "us-west1"
CREDS = "key.json"
PROJECTID = "mismatch"
BUCKET = "mismatch-test"

class Vision(unittest.TestCase):
    def test_detectLabels(self):
        imgPath = os.path.join(os.path.dirname(__file__), './data/skirt.jpg')
        print(detectLabels(imgPath))
    def test_detectObjects(self):
        imgPath = os.path.join(os.path.dirname(__file__), './data/skirt.jpg')
        print(detectObjects(imgPath))

if __name__ == '__main__':
    unittest.main()