"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""

from datetime import date
from abc import ABC

class Track(ABC):
    """Abstract base class for all playable content"""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str) -> None:
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self) -> float:
        """Returns the duration of the track in minutes"""
        return self.duration_seconds / 60.0

    def __eq__(self, other: object) -> bool:
        """Check if two tracks are equal by id"""
        if hasattr(other, "track_id"):
            return self.track_id == getattr(other, "track_id")
        return False

class Song(Track):
    """Music track associated with an artist"""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist

class SingleRelease(Song):
    """Song released as standalone singler"""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist, release_date: date) -> None:
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date

class AlbumTrack(Song):
    """Song that is part of an album"""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist, track_number: int, album=None) -> None:
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = album

class Podcast(Track):
    """Podcast episode"""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, description: str = "") -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description

class InterviewEpisode(Podcast):
    """Interview-format podcast"""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, guest: str, description: str = "") -> None:
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest

class NarrativeEpisode(Podcast):
    """Narrative-format podcast"""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, season: int, episode_number: int, description: str = "") -> None:
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number

class AudiobookTrack(Track):
    """Chapter from an audiobook"""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, author: str, narrator: str) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator