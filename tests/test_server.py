import unittest

from flask import Flask, redirect, request
from flask_socketio import SocketIO, emit
from lib.Queue import Queue
from lib.Song import Song
from lib.spotify import get_request, create_song
import requests as http
import json
import redis as rd
from base64 import b64encode

class TestServerFunctions(unittest.TestCase):

    def setUp(self):

    def test_callback(self):

    def test_authenticate(self):
        
    def test_add_song(self):
        
    def test_get_next_song(self):

    def test_resume(self):
        
    def test_pause(self):

    def test_searchbar_changed(self):

    def test_thumbs_change(self):

    def test_queue_change(self):
