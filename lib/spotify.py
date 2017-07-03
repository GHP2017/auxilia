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
