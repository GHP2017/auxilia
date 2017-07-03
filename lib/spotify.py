import requests as http
import redis as rd
from lib.Song import Song

track_uri = 'https://api.spotify.com/v1/tracks/'
cache = rd.StrictRedis(host='localhost', port=6379, db=0)

def get_request(url, call_type='GET', body=None):
    access_token = cache.get('access_token').decode('utf-8')
    if call_type is 'GET':
        response = http.get(url, headers={'Authorization': 'Bearer ' + access_token})
        if int(response.status_code) >= 400:
            print(response.status_code)
            refresh_access_token()
            response = http.get(url, headers={'Authorization': 'Bearer ' + access_token})
    if call_type is 'POST':
        response = http.post(url, data=body, headers={'Authorization': 'Bearer ' + access_token})
        print(response.text)
        if int(response.status_code) >= 400:
            refresh_access_token()
            response = http.post(url, data=body, headers={'Authorization': 'Bearer ' + access_token})
    if call_type is 'PUT':
        response = http.put(url, data=body, headers={'Authorization': 'Bearer ' + access_token})
        print(response.text, response.status_code)
        if int(response.status_code) >= 400:
            refresh_access_token()
            response = http.put(url, data=body, headers={'Authorization': 'Bearer ' + access_token})

    return response


def refresh_access_token():
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': cache.get('refresh_token').decode('utf-8')
    }
    string = (client_id + ':' + client_secret).encode('utf-8')
    encoded_string = str(b64encode(string))
    response = http.post(token_uri, data=body, headers={'Authorization': 'Basic ' + encoded_string})
    data = response.json()
    
    cache.set('access_token', data['access_token'])

# takes either a track id or a track object as returned by the spotify api
def create_song(track):
    if type(track) is str:
        min_track_id = track[14:]
        response = get_request(track_uri + min_track_id)
        data = response.json()
    else:
        data = track
    track_id = data['id']
    track_name = data['name']
    track_artists = ','.join(artist['name'] for artist in data['artists'])
    album_uri = data['album']['images'][0]['url']
    album_name = data['album']['name']
    duration = data['duration_ms']
    return Song(track_name, track_id, track_artists, album_uri, album_name, duration, False)

def get_implicit_songs(seeds, num):
    return create_song("spotify:track:0VgkVdmE4gld66l8iyGjgx")
