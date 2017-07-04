from lib.Song import Song
import ast

class Queue:

    def __init__(self, cache): 
        self.cache = cache
        self.cache.set('queue', [])
        self.cache.set('history', [])

    def addSong(self, song):
        queue = self.instantiate_queue()
        queue.append(song.to_dict())
        self.sortSongs(queue)
        self.cache.set('queue', queue)

    def addImplicit(self, songs):
        queue = self.instantiate_queue()
        if len(queue)<5:
            num=5-len(queue)
            new_songs=get_implicit_songs(songs, num)
            queue.extend(new_songs)
            self.cache.set('queue', queue)                

    def getSong(self):
        queue = self.instantiate_queue()
        song_data = queue.pop(0)

        history = self.instantiate_history()
        history.append(song_data)
        
        self.ageSongs(queue)
        self.calculateScore(queue)
        self.sortSongs(queue)

        self.cache.set('queue', queue)
        self.cache.set('history', history)

        keys = ['name', 'track_id', 'artist', 'album_uri', 'album_name', 'duration', 'suggested']
        args = [song_data[key] for key in keys]
        return Song(*args)

    def sortSongs(self, queue):
        queue.sort(key = lambda x: x['score'])

    def calculateScore(self, queue):
        for song in queue:
            song['score'] = song['age']**1.5 + song['upvotes'] - song['downvotes']
        
    def ageSongs(self, queue):
        for song in queue:
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
        
