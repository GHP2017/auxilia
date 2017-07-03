import requests as http
from mouse import Mouse
import time

m = Mouse()
song_url = 'http://127.0.0.1:5000/get_next_song'
response = http.get(song_url)
data = response.json()
duration = data['duration'] * 1000
now = time.time()
m.playSong(data['track_id'])
