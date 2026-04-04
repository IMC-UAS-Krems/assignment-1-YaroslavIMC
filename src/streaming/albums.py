"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""

class Album:
    def __init__(self, album_id: str, title: str, artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track):
        track.album = self
        self.tracks.append(track)
        self.tracks.sort(key=lambda item: item.track_number)

    def track_ids(self):
        answer = set()
        for track in self.tracks:
            answer.add(track.track_id)
        return answer

    def duration_seconds(self):
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total