import unittest
import ast

class TestQueueFunctions(unittest.TestCase):
    def setUp(self):
        cache = rd.StrictRedis(host='localhost', port=6379, db=0)
        self.cache = cache
        self.cache.set('queue', [])
        self.cache.set('history', [])
        queue=self.instantiate_queue()
    
    def test_calculate_score(self):
        
    def test_age_songs(self):
