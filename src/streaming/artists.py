"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

class Artist:
    """Music artist or content creator"""
    def __init__(self, artist_id: str, name: str, genre: str):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = []

    def add_track(self, track):
        if track not in self.tracks:
            self.tracks.append(track)

    def track_count(self):
        return len(self.tracks)