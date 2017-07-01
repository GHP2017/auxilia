from flask import Flask, redirect, request
from flask_socketio import SocketIO
import os
import requests as http
import json
from base64 import b64encode

app = Flask(__name__)
socketio = SocketIO(app)

client_id = 'f3b0c51df1124cc985fd4012b6d55d95'
client_secret = 'e54ca2e0bf394944a1247830443dba3c'

redirect_uri = 'http://127.0.0.1:5000/callback'
#redirect_uri = 'https://example-django-app-dude0faw3.c9users.io/callback'

authorize_uri = 'https://accounts.spotify.com/authorize'
token_uri = 'https://accounts.spotify.com/api/token'
play_uri = 'https://api.spotify.com/v1/me/player/play'
pause_uri = 'https://api.spotify.com/v1/me/player/pause'

code = ''
token = ''

## OAUTH2 

def get_request(url, call_type='GET', body=None):
    print(os.environ['ACCESS_TOKEN'])
    if call_type is 'GET':
        response = http.get(url, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})
        if int(response.status_code) >= 400:
            refresh_access_token()
            response = http.get(url, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})
    if call_type is 'POST':
        response = http.post(url, data=body, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})
        print(response.text)
        if int(response.status_code) >= 400:
            refresh_access_token()
            response = http.post(url, data=body, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})
    if call_type is 'PUT':
        response = http.put(url, data=body, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})
        print(response.text, response.status_code)
        if int(response.status_code) >= 400:
            refresh_access_token()
            response = http.put(url, data=body, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})

    return response


def refresh_access_token():
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': os.environ['REFRESH_TOKEN']
    }
    string = (client_id + ':' + client_secret).encode('utf-8')
    encoded_string = str(b64encode(string))
    response = http.post(token_uri, data=body, headers={'Authorization': 'Basic ' + encoded_string})
    data = response.json()
    print(data)
    access_token = data['access_token']
    os.environ['ACCESS_TOKEN'] = access_token


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
    print(data)
    token = data['access_token']
    refresh = data['refresh_token']
    print(token)

    os.environ['REFRESH_TOKEN'] = refresh
    os.environ['ACCESS_TOKEN'] = token

    return redirect('/static/play.html')
    
@app.route("/authenticate")
def authenticate():
    return redirect(authorize_uri + '?client_id=' + client_id + \
                    '&response_type=code&redirect_uri=' + redirect_uri + '&scope=user-library-read user-modify-playback-state')

## Queue 

@app.route("/add_song")
def add_song():
    song = request.args.get('song')
    print(get_request(play_uri, body=json.dumps({'uris': [song]}), call_type='PUT'))
    return 'success'

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


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == "__main__":
    socketio.run(app)