class Song:
    def __init__(self, name, ID, artist, album, suggested):
        self.name = name
        self.ID = ID
        self.artist = artist
        self.album = album
        self.score = 0
        self.upvotes = 0
        self.downvotes = 0
        self.age = 0
        self.suggested = suggested

    def incrementScore(self):
        self.score = self.score + 1

    def decrementScore(self):
        self.score = self.score - 1

    def debugPrint(self):
        return "name: " + self.name + "\nartist: " + self.artist
