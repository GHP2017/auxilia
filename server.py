from flask import Flask, redirect, request, render_template, session
from flask_socketio import SocketIO, emit
from lib.Queue import Queue, OptionsConflict
from lib.Song import Song
from lib.User import User
import os
from datetime import timedelta
from lib.spotify import get_request, create_song
import requests as http
import json
from time import time
import redis as rd
import ast
from base64 import b64encode
from uuid import uuid4

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=6)

socketio = SocketIO(app)
cache = rd.StrictRedis(host='localhost', port=6379, db=0)
options = {
    'safe_mode': 'False',
    'downvotes_threshold': '3',
    'max_individual_songs': '3'
}

cache.set('paused_time', 0)
cache.set('is_paused', 'False')
cache.set('options', options)
cache.set('refresh_token', 'AQBaMZ434eYXxTv8aXProOYllKxIIhT3QmO27-Wrie4EhzD1jZYodny3_G2bc0CMUigTc79ZQ_EK5FNJqImG52tPvu0kO6C13NFTZXUVW2N6pLKAZOlC3g9tWUNL302gkvw')

queue = Queue(cache)

client_id = 'f3b0c51df1124cc985fd4012b6d55d95'
client_secret = 'e54ca2e0bf394944a1247830443dba3c'

#redirect_uri = 'http://127.0.0.1:5000/callback'
redirect_uri = 'http://172.16.49.80:5000/callback'
#redirect_uri = 'https://example-django-app-dude0faw3.c9users.io/callback'

authorize_uri = 'https://accounts.spotify.com/authorize'
token_uri = 'https://accounts.spotify.com/api/token'

play_uri = 'https://api.spotify.com/v1/me/player/play'
pause_uri = 'https://api.spotify.com/v1/me/player/pause'
track_uri = 'https://api.spotify.com/v1/tracks/'
search_uri = 'https://api.spotify.com/v1/search?type=track&limit=20&q='

 ## Main Pages

@app.route('/')
def landing():
    """Returns the landing page"""
    return app.send_static_file('landing.html')

@app.route('/play')
def play_page():
    """Returns the play page"""
    session.permanent = True
    if 'tracks' not in session:
        session['tracks'] = {}
    if 'id' not in session:
        session['id'] = uuid4().int
    return app.send_static_file('play.html')

## Admin

@app.route('/admin')
def admin():
    return app.send_static_file('admin.html')

@app.route('/options', methods=['GET', 'POST'])
def options():
    if request.method == 'GET':
        return json.dumps(queue.instantiate_options())
    else:
        options = queue.instantiate_options()
        keys = request.form.keys()
        for key in keys:
            options[key] = request.form[key]
        print(options)
        cache.set('options', options)
        return json.dumps({'msg': 'success'})

## Queue

@app.route("/add_song")
def add_song():
    """Creates song object, adds to queue, and updates queue. Returns success upon completion."""
    options = queue.instantiate_options()
    raw_queue = queue.instantiate_queue()
    track_id = request.args.get('song')

    for song in raw_queue:
        if song['track_id'] == track_id[14:]:
            return json.dumps({'error': 'Cannot add a song already in the queue'})

    num_songs_added = 0
    for song in raw_queue:
        if song['added_by'] == session['id']:
            num_songs_added += 1

    if num_songs_added >= int(options['max_individual_songs']):
        print('user reached max songs')
        return json.dumps({'error': "You are not allowed to add any more songs until one plays"})

    song_obj = create_song(track_id, added_by=session['id'])
    queue.addSong(song_obj)
    queue_change()
    return json.dumps({'success': 'added ' + track_id})

@app.route('/get_next_song')
def get_next_song():
    """Retrieves next song in queue, updates queue, and returns the next song as JSON"""
    try:
        next_song = queue.getSong()
        queue_change()
        currently_playing_change(next_song)
        return json.dumps(next_song.to_dict())
    except IndexError as e:
        return json.dumps({'error': 'No songs in the queue'})

@app.route('/thumbs_change', methods=['POST'])
def thumbs_change():
    print('thumbs change')
    data = request.form
    """Changes queue when thumbs up/down."""
    user = User(session['id'])
    user.save_thumbs_change(data['track_id'], data['change'])
    queue.thumbs_change(data['track_id'], data['change'], decrement=(data['decrement'] == 'true'))
    queue_change()
    return json.dumps({'success': 'acknowledged the upvote/downvote'})

# uses the session obj to update client side data upon connection
@app.route('/connect')
def connect():
    try:
        user = User(session['id'])
        print(user)
        return json.dumps(user.get_data()['thumbs_tracks'])
    except AttributeError:
        return json.dumps({'error': 'no data for this user yet'})

## Playback

@app.route('/playback')
def playback():
    """changes playback state to paused or resume, and returns acknowlegment"""
    state = request.args.get('state')
    if state == 'paused':
        paused()
    elif state == 'resume':
        resume()
    return json.dumps({'msg': 'playback change acknowledged'})

## HTTP Error Handling
"""
@app.errorhandler(403)
def forbidden():
    return render_template('403.html')

@app.errorhandler(404)
def page_not_found():
    return render_template('404.html')

@app.errorhandler(500) #must turn off debugging mode in order to use this custom error handling
def internal_error(error):
    return '500 Error'

"""

## Websocket Events

@socketio.on('client_connected')
def client_connected(data):
    """When client joins, syncs changes in queue, history and playback."""
    print('a client connected')
    emit('queue_changed', queue.serialize())
    history = queue.instantiate_history()
    if len(history) > 0:
        song_data = history[-1]
        emit('mid_currently_playing', song_data)
    if cache.get('is_paused').decode('utf-8') == 'True':
        pause_time = int(cache.get('paused_time').decode('utf-8'))
        socketio.emit('paused', pause_time)

@socketio.on('searchbar_changed')
def searchbar_changed(data):
    """Searches for user's input in the searchbar, and creates results list"""
    print('searching for ' + data['query'])
    if data['query'] != '':
        options = queue.instantiate_options()
        print(options)
        query = data['query'].replace(' ', '+')
        response = get_request(search_uri + query)
        songs = []
        is_explicit_list = []

        for track_obj in response.json()['tracks']['items']:
            song_obj, is_explicit = create_song(track_obj, return_is_explicit=True)
            songs.append(song_obj)
            is_explicit_list.append(is_explicit)
        
        if options['safe_mode'] == 'true':
            print('safe mode???')
            temp_songs = []
            for i in range(len(songs)):
                if not is_explicit_list[i]:
                    temp_songs.append(songs[i])
            songs = temp_songs

        if len(songs) > 5:
            songs = songs[:5]

        serialized_songs = [song.to_dict() for song in songs]
        emit('suggestions_changed', serialized_songs)

def queue_change():
    """Emits queue_changed"""
    socketio.emit('queue_changed', queue.serialize())
    
def currently_playing_change(song):
    """Emits a change in the song playing."""
    socketio.emit('currently_playing_changed', song.to_dict())

def paused():
    """Records time of pause, adjusts cache accordingly, and emits paused signal"""
    pause_time = time()
    cache.set('paused', pause_time)
    socketio.emit('paused', pause_time)

def resume():
    """Sets is_paused to False, and emits resume signal."""
    cache.set('is_paused', 'False')
    socketio.emit('resume', {})

## OAUTH2 

@app.route("/callback")
def callback():
    """Returns a redirect to index after posting data, and setting access and refresh tokens."""
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

    return redirect('/')
    
@app.route("/authenticate")
def authenticate():
    """Returns a redirect to authenticate user."""
    try:
        return redirect(authorize_uri + '?client_id=' + client_id + \
                    '&response_type=code&redirect_uri=' + redirect_uri + '&scope=user-library-read user-modify-playback-state')
    except Exception as e:
        return ('authenticate() threw ' +str(e))

## Testing only

@app.after_request
def add_header(r):
    """For testing, doesn't store cache."""
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')