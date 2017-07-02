from lib.Song import Song

class Queue:

    def __init__(self): 
        self.queue = []
        self.played = []

    def addSong(self, song):
        self.queue.append(song)
        self.sortSongs()

    def getSong(self):
        song = self.queue.pop(0)
        self.played.append(song)
        self.ageSongs()
        self.calculateScore()
        self.sortSongs()
        return song

    def sortSongs(self):
        self.queue.sort(key = lambda x: x.score)

    def calculateScore(self, song):
        song.score = age**1.5 + upvotes - downvotes
        
    def ageSongs(self):
        for song in self.queue:
            song.age = song.age + 1

    def serialize(self):
        return [song.to_dict() for song in self.queue]
