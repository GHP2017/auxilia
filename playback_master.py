import requests as http
from lib.mouse import Mouse
from lib.GPIOInteraction import GPIOInteractor
import time

# called whenever the physical pause/play button is pressed
def toggle_play_pause():
    if(playing):
        m.pause()
        playing = False
        paused_at = time.time()
    elif(not playing):
        m.play()
        playing = True
        pause_time += time.time() - paused_at

pause_time = 0
paused_at = None
playing = False
m = Mouse()
g = GPIOInteractor()
g.setButtonCallback(toggle_play_pause)
song_url = 'http://127.0.0.1:5000/get_next_song'
response = http.get(song_url)

def get_next_song():
    ## TODO:
    # add error handling here
    return http.get(song_url).json()


        
# establish a connection
"""
while response.status_code != 200:
    time.sleep(10)
    response = http.get(song_url)
"""
    
data = response.json()
duration = data['duration'] * 1000
start_time = time.time()
m.playSong(data['track_id'])
playing = True
# main loop
while True:
    if time.time() - start_time - pause_time >= duration:
        data = get_next_song()
        duration = data['duration'] * 1000
        m.playSong(data['track_id'])
        start_time = time.time()
        pause_time = 0
