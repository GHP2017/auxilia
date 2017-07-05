from flask import Flask, redirect, request, render_template
from flask_socketio import SocketIO, emit
from lib.Queue import Queue
from lib.Song import Song
from lib.spotify import get_request, create_song
import requests as http
import json
import redis as rd
from base64 import b64encode

app = Flask(__name__)
socketio = SocketIO(app)
cache = rd.StrictRedis(host='localhost', port=6379, db=0)
queue = Queue(cache)

client_id = 'f3b0c51df1124cc985fd4012b6d55d95'
client_secret = 'e54ca2e0bf394944a1247830443dba3c'

#redirect_uri = 'http://127.0.0.1:5000/callback'
redirect_uri = 'http://172.16.33.88:5000/callback'
#redirect_uri = 'https://example-django-app-dude0faw3.c9users.io/callback'

authorize_uri = 'https://accounts.spotify.com/authorize'
token_uri = 'https://accounts.spotify.com/api/token'

play_uri = 'https://api.spotify.com/v1/me/player/play'
pause_uri = 'https://api.spotify.com/v1/me/player/pause'
track_uri = 'https://api.spotify.com/v1/tracks/'
search_uri = 'https://api.spotify.com/v1/search?type=track&limit=5&q='

## OAUTH2 

@app.route("/callback")
def callback():
    code = request.args.get('code')
    result = http.post(token_uri, data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    })
    data = result.json()
    
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    
    cache.set('access_token', access_token)
    cache.set('refresh_token', refresh_token)

    return redirect('/static/play.html')
    
@app.route("/authenticate")
def authenticate():
    return redirect(authorize_uri + '?client_id=' + client_id + \
                    '&response_type=code&redirect_uri=' + redirect_uri + '&scope=user-library-read user-modify-playback-state')

## Queue 

@app.route("/add_song")
def add_song():
    try:
        track_id = request.args.get('song')
        song_obj = create_song(track_id)
        queue.addSong(song_obj)
        queue_change()
        return 'success'
    except Exception as e:
        return(str(e))

@app.route('/get_next_song')
def get_next_song():
    next_song = queue.getSong()
    print(type(next_song))
    queue_change()
    return json.dumps(next_song.to_dict())

## Error Handling
@app.errorhandler(404)
def page_not_found():
    return render_template('404.html')

@app.errorhandler(500) #must turn off debugging mode in order to use this custom error handling
def internal_error(error):
    return '500 Error'

## Playback Endpoints

@app.route("/resume")
def resume():
    print(get_request(play_uri, call_type='PUT'))
    return 'success'

@app.route("/pause")
def pause():
    print('GOT PAUSE')
    print(get_request(pause_uri, call_type='PUT'))
    return 'success'

## Websocket Events

@socketio.on('client_connected')
def client_connected(data):
    print('a client connected')
    emit('queue_changed', queue.serialize())

@socketio.on('searchbar_changed')
def searchbar_changed(data):
    print('searchbar changing...')
    print('searching for ' + data['query'])
    query = data['query'].replace(' ', '+')
    response = get_request(search_uri + query)
    songs = []
    for track_obj in response.json()['tracks']['items']:
        songs.append(create_song(track_obj))
    serialized_songs = [song.to_dict() for song in songs]
    emit('suggestions_changed', serialized_songs)

@socketio.on('thumbs_change')
def thumbs_change(data):
    print('song got thumbs up or thumbs down')
    queue.thumbs_change(data['track_id'], data['change'])
    queue_change()

def queue_change():
    socketio.emit('queue_changed', queue.serialize())

## Testing only

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')