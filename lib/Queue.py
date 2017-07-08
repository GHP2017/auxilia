from lib.Song import Song
from lib.spotify import get_implicit_songs
import ast
from time import time
from copy import deepcopy

class Queue:

    def __init__(self, cache): 
        self.cache = cache
        self.cache.set('queue', [])
        self.cache.set('history', [])

    def addSong(self, song):
        queue = self.instantiate_queue()
        history = self.instantiate_history()
        index = None
        queue = [song for song in queue if song['explicit']]
        queue.append(song.to_dict())

        if len(queue) < 5:
            self.addImplicit(queue, history, fallback_song=song.to_dict())
        
        self.sortSongs(queue)
        self.cache.set('queue', queue)

    def getSong(self):
        queue = self.instantiate_queue()
        song_data = queue.pop(0)

        history = self.instantiate_history()
        history_song_data = deepcopy(song_data)
        history_song_data['time_played'] = time() + 5
        history.append(history_song_data)

        if len(queue) < 5:
            self.addImplicit(queue, history)
        
        self.ageSongs(queue)
        self.calculateScore(queue)
        self.sortSongs(queue)

        self.cache.set('queue', queue)
        self.cache.set('history', history)

        keys = ['name', 'track_id', 'artist', 'album_uri', 'album_name', 'duration', 'explicit', 'valence', 'energy']
        args = [song_data[key] for key in keys]
        return Song(*args)

    def addImplicit(self, queue, history, fallback_song=None):
        song_seeds = []

        for song in history:
            if song['explicit']:
                song_seeds.append(song)
        
        if len(song_seeds) < 5:
            for song in queue:
                if song['explicit']:
                    song_seeds.append(song)

        if len(song_seeds) > 5:
            song_seeds = song_seeds[:5]

        if len(song_seeds) is 0:
            song_seeds = [fallback_song]
        
        num = 5 - len(queue)
        new_songs = get_implicit_songs(song_seeds, num)
        queue.extend(new_songs)

    def thumbs_change(self, track_id, change, decrement=False):
        queue = self.instantiate_queue()
        
        changing_song = None
        for song in queue:
            if song['track_id'] == track_id:
                changing_song = song
                break

        if change == 'up':
            if not changing_song['explicit']:
                changing_song['explicit'] = True
            if decrement:
                changing_song['upvotes'] += -1
            else:
                changing_song['upvotes'] += 1
        else:
            if decrement:
                changing_song['downvotes'] += -1
            else:
                changing_song['downvotes'] += 1

        self.calculateScore(queue)
        self.sortSongs(queue)

        self.cache.set('queue', queue)

    def sortSongs(self, queue):
        queue.sort(key = lambda x: x['score'], reverse=True)

    def calculateScore(self, queue):
        for song in queue:
            if song['explicit']:
                song['score'] = 3 * song['age'] + 2 * song['upvotes'] - 2 * song['downvotes']
            else:
                song['score'] = -1 * song['downvotes']
        
    def ageSongs(self, queue):
        for song in queue:
            if song['explicit']:
                song['age'] += 1

    def instantiate_queue(self):
        serialized_queue = self.cache.get('queue')
        queue = ast.literal_eval(serialized_queue.decode('utf-8'))
        return queue

    def instantiate_history(self):
        serialized_history = self.cache.get('history')
        history = ast.literal_eval(serialized_history.decode('utf-8'))
        return history

    def serialize(self):
        return self.instantiate_queue()
        
