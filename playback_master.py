import requests as http
from lib.mouse import Mouse
import time

m = Mouse()
song_url = 'http://127.0.0.1:5000/get_next_song'
response = http.get(song_url)

def get_next_song():
    ## TODO:
    # add error handling here
    return http.get(song_url).json()

# establish a connection
while response.status_code != 200:
    sleep(10)
    response = http.get(song_url)
    
data = response.json()
duration = data['duration'] * 1000
start_time = time.time()
m.playSong(data['track_id'])

# main loop
while True:
    if time.time() - start_time >= duration:
        data = get_next_song()
        duration = data['duration'] * 1000
        m.playSong(data['track_id'])
        start_time = time.time()
