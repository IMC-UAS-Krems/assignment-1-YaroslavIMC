"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

from datetime import datetime, timedelta

from streaming.tracks import Song
from streaming.playlists import CollaborativePlaylist


class StreamingPlatform:
    def __init__(self, name:str):
        self.name = name
        self.catalogue = {}
        self.users = {}
        self.artists = {}
        self.albums = {}
        self.playlists = {}
        self.sessions = []

    def add_track(self, track):
        self.catalogue[track.track_id] = track

    def add_user(self, user):
        self.users[user.user_id] = user

    def add_artist(self, artist):
        self.artists[artist.artist_id] = artist

    def add_album(self, album):
        self.albums[album.album_id] = album

    def add_playlist(self, playlist):
        self.playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self.sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id):
        return self.catalogue.get(track_id)

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_artist(self, artist_id):
        return self.artists.get(artist_id)

    def get_album(self, album_id):
        return self.albums.get(album_id)

    def all_users(self):
        return list(self.users.values())

    def all_tracks(self):
        return list(self.catalogue.values())
