class Song:
    # explicit refers to this song being purposefully added by a user,
    # as opposed to by algorithm
    def __init__(self, name, track_id, artist, album_uri, album_name, duration, added_by=None, explicit=False, valence=None, energy=None):
        self.name = name
        self.track_id = track_id
        self.artist = artist
        self.album_uri = album_uri
        self.album_name = album_name
        self.duration = duration
        self.score = 0
        if explicit:
            self.upvotes = 1
        else:
            self.upvotes = 0
        self.downvotes = 0
        self.added_by = added_by
        self.age = 0
        self.explicit = explicit
        self.valence = valence
        self.energy = energy

    def to_dict(self):
        """Returns Song args/parameters."""
        return {
            'name': self.name,
            'track_id': self.track_id,
            'artist': self.artist,
            'album_uri': self.album_uri,
            'album_name': self.album_name,
            'duration': self.duration,
            'score': self.score,
            'added_by': self.added_by,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'age': self.age,
            'explicit': self.explicit,
            'valence': self.valence,
            'energy': self.energy
        }
