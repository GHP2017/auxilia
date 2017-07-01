import operator
from SongClass import Song

class Queue:

    def __init__(self): 
        self.queue = []
        self.played = []

    def addSong(self, song):
        self.queue.append(song)
        sortSongs()

    def getSong(self):
        song = self.queue.pop(0)
        self.played.append(song)
        ageSongs()
        calculateScore()
        sortSongs()
        return song

    def sortSongs(self):
        self.queue.sort(key = lambda x: x.score)

    def calculateScore(self, song):
        song.score = age**1.5 + upvotes - downvotes
        
    def ageSongs(self):
        for song in self.queue:
            song.age = song.age + 1
