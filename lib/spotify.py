from lib.Song import Song
import requests as http
import redis as rd
from base64 import b64encode
import statistics

cache = rd.StrictRedis(host='localhost', port=6379, db=0)

client_id = 'f3b0c51df1124cc985fd4012b6d55d95'
client_secret = 'e54ca2e0bf394944a1247830443dba3c'

token_uri = 'https://accounts.spotify.com/api/token'

track_uri = 'https://api.spotify.com/v1/tracks/'
recommendations_uri = 'https://api.spotify.com/v1/recommendations?seed_tracks='

def get_request(url, call_type='GET', body=None):
    access_token = cache.get('access_token').decode('utf-8')
    if call_type is 'GET':
        response = http.get(url, headers={'Authorization': 'Bearer ' + access_token})
        ## TODO:
        # change for different responses; invalid client, malformed request, etc.
        if int(response.status_code) >= 400:
            print(response.status_code)
            print(response.text)
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
def create_song(track, explicit=True):
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
    return Song(track_name, track_id, track_artists, album_uri, album_name, duration, explicit)

def get_implicit_songs(seeds, num):
    songs = ','.join([song['track_id'] for song in seeds])
    response = get_request(recommendations_uri + songs + '&limit=' + str(num))
    data = response.json()
    return [create_song(track_obj, explicit=False).to_dict() for track_obj in data['tracks']]

def get_medians(seeds):
    median_valence = statistics.median(song['valence'] for song in seeds)
    median_energy = statistics.median(song['energy'] for song in seeds)
    response = '&target_valence=' + median_valence + '&target_energy' + median_energy
    return response
