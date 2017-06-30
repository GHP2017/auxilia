from flask import Flask, redirect, request
import os
import requests as http

app = Flask(__name__)

client_id = 'f3b0c51df1124cc985fd4012b6d55d95'
client_secret = 'e54ca2e0bf394944a1247830443dba3c'

redirect_uri = 'http://127.0.0.1:5000/callback'
authorize_uri = 'https://accounts.spotify.com/authorize'
token_uri = 'https://accounts.spotify.com/api/token'
play_uri = 'https://api.spotify.com/v1/me/player/play'
pause_uri = 'https://api.spotify.com/v1/me/player/pause'

code = ''
token = ''

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
    print('token result')
    print(result.json())
    dict = result.json()

    token = dict['access_token']
    os.environ['TOKEN'] = token

    return redirect('/static/play.html')
    
@app.route("/authenticate")
def authenticate():
    return redirect(authorize_uri + '?client_id=' + client_id + \
                    '&response_type=code&redirect_uri=' + redirect_uri + '&scope=user-library-read user-modify-playback-state')

## Queue 

@app.route("/add_song")
def add_song():
    pass

## Playback Endpoints

@app.route("/resume")
def resume():
    print(http.put(play_uri, headers={'Authorization': 'Bearer ' + os.environ['TOKEN']}))
    return 'success'

@app.route("/pause")
def pause():
    print(http.put(pause_uri, headers={'Authorization': 'Bearer ' + os.environ['TOKEN']}))
    return 'success'




if __name__ == "__main__":
    app.run()