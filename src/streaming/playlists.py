"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

class Playlist:
    """User-curated ordered collection of tracks"""
    def __init__(self, playlist_id: str, name: str, owner) -> None:
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []

    def add_track(self, track) -> None:
        """Adds a track to the playlist"""
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_id: str) -> None:
        """Removes a track from the playlist"""
        new_tracks = []
        for track in self.tracks:
            if track.track_id != track_id:
                new_tracks.append(track)
        self.tracks = new_tracks

    def total_duration_seconds(self) -> int:
        """Returns the total duration of the playlist in seconds"""
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total

class CollaborativePlaylist(Playlist):
    """Playlist with multiple contributors"""
    def __init__(self, playlist_id: str, name: str, owner) -> None:
        super().__init__(playlist_id, name, owner)
        self.contributors = [owner]

    def add_contributor(self, user) -> None:
        """Adds a contributor to the playlist"""
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user) -> None:
        """Removes a contributor if not owner"""
        if user == self.owner:
            return
        if user in self.contributors:
            self.contributors.remove(user)