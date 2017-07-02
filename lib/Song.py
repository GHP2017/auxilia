class Song:
    def __init__(self, name, track_id, artist, album_uri, album_name, suggested):
        self.name = name
        self.track_id = track_id
        self.artist = artist
        self.album_uri = album_uri
        self.album_name = album_name
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

    def to_dict(self):
        return {
            'name': self.name,
            'track_id': self.track_id,
            'artist': self.artist,
            'album_uri': self.album_uri,
            'album_name': self.album_name,
            'score': self.score,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'age': self.age,
            'suggested': self.suggested
        }
