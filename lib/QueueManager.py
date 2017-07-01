import operator
from SongClass import Song

queue = []
playing = None
played = []

def addSongToQueue(song):
    if(len(queue)>0):
        queue.append(song)
    else:
        playing = song
    sortSongs()

def shiftNextSong():
    played.append(playing)
    playing = queue.pop(0)
    ageSongs()
    return playing

def sortSongs():
    queue.sort(key = lambda x: x.score)

def calculateScore(song):
    song.score = age**1.5 + upvotes - downvotes
    
def ageSongs():
    for song in queue:
        song.age = song.age + 1
        
def test():
    queue.append(Song("Songname","1234523","Drew Cutchins","My Album",False))
    for song in queue:
        print song.debugPrint()
