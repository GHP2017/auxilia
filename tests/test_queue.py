import unittest
from lib.Song import Song
import ast

class TestQueueFunctions(unittest.TestCase):
    def setUp(self):
        cache = rd.StrictRedis(host='localhost', port=6379, db=0)
        self.cache = cache
        self.cache.set('queue', [])
        self.cache.set('history', [])
    