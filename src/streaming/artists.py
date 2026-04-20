"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

class Artist:
    """Music artist or content creator"""
    def __init__(self, artist_id: str, name: str, genre: str) -> None:
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = []

    def add_track(self, track) -> None:
        """Add a track to the artist"""
        if track not in self.tracks:
            self.tracks.append(track)

    def track_count(self) -> int:
        """Return the number of tracks for the artist"""
        return len(self.tracks)