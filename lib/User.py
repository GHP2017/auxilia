import redis as rd
import json

class User:

    def __init__(self, id):
        self.id = id
        self.cache = rd.StrictRedis()

    def save_thumbs_change(self, track_id, change):
        try:
            data = self.get_data()
        except AttributeError:
            # must be no data yet
            data = {'thumbs_tracks': {}}
        tracks = data['thumbs_tracks']
        tracks[track_id] = {
            'was_upvoted': False,
            'was_downvoted': False
        }

        if change == 'up':
            tracks[track_id]['was_upvoted'] = not tracks[track_id]['was_upvoted']
        else: 
            tracks[track_id]['was_downvoted'] = not tracks[track_id]['was_downvoted']

        self.save_data(data)

    def get_data(self):
        data = self.cache.get(self.id)
        return json.loads(data.decode('utf-8'))

    def save_data(self, data):
        data = json.dumps(data)
        self.cache.set(self.id, data)

        
