"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

from datetime import datetime, timedelta
from streaming.tracks import Song, Track
from streaming.playlists import CollaborativePlaylist, Playlist
from streaming.users import PremiumUser, FamilyMember, User
from streaming.artists import Artist
from streaming.albums import Album
from streaming.sessions import ListeningSession

class StreamingPlatform:
    """Central platform orchestrating all entities"""
    def __init__(self, name:str) -> None:
        self.name = name
        self.catalogue = {}
        self.users = {}
        self.artists = {}
        self.albums = {}
        self.playlists = {}
        self.sessions = []

    def add_track(self, track) -> None:
        """Add a track to the platform"""
        self.catalogue[track.track_id] = track

    def add_user(self, user) -> None:
        """Add a user to the platform"""
        self.users[user.user_id] = user

    def add_artist(self, artist) -> None:
        """Add an artist to the platform"""
        self.artists[artist.artist_id] = artist

    def add_album(self, album) -> None:
        """Add an album to the platform"""
        self.albums[album.album_id] = album

    def add_playlist(self, playlist) -> None:
        """Add a playlist to the platform"""
        self.playlists[playlist.playlist_id] = playlist

    def record_session(self, session) -> None:
        """Record a session"""
        self.sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id) -> Track | None:
        """Return a track from the platform"""
        return self.catalogue.get(track_id)

    def get_user(self, user_id) -> User | None:
        """Return a user from the platform"""
        return self.users.get(user_id)

    def get_artist(self, artist_id) -> Artist | None:
        """Return an artist from the platform"""
        return self.artists.get(artist_id)

    def get_album(self, album_id) -> Album | None:
        """Return an album from the platform"""
        return self.albums.get(album_id)

    def all_users(self) -> list[User]:
        """Return a list of all users"""
        return list(self.users.values())

    def all_tracks(self) -> list[Track]:
        """Return a list of all tracks"""
        return list(self.catalogue.values())

    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        """Returns total listening time in minutes"""
        total = 0.0
        for session in self.sessions:
            if start <= session.timestamp <= end:
                total += session.duration_listened_seconds / 60.0
        return total

    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        """Returns average number of unique tracks for premium users"""
        premium_users = []

        for user in self.users.values():
            if type(user) is PremiumUser:
                premium_users.append(user)
        if len(premium_users) == 0:
            return 0.0

        now = datetime.now() - timedelta(days=days)
        total_unique = 0
        for user in premium_users:
            unique_track_ids = set()
            for session in user.sessions:
                if session.timestamp >= now:
                    unique_track_ids.add(session.track.track_id)
            total_unique += len(unique_track_ids)

        return total_unique / len(premium_users)

    def track_with_most_distinct_listeners(self) -> Track | None:
        """Returns track with most distinct listeners"""
        if len(self.sessions) == 0:
            return None

        best_track = None
        best_count = -1

        for track in self.catalogue.values():
            listeners = set()
            for session in self.sessions:
                if session.track.track_id == track.track_id:
                    listeners.add(session.user.user_id)
            if len(listeners) > best_count:
                best_count = len(listeners)
                best_track = track

        return best_track

    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        """Returns average session duration grouped by user type"""
        values = {}

        for session in self.sessions:
            type_name = type(session.user).__name__
            if type_name not in values:
                values[type_name] = []
            values[type_name].append(session.duration_listened_seconds)

        answer = []
        for type_name, durations in values.items():
            average = sum(durations) / len(durations)
            answer.append((type_name, float(average)))

        answer.sort(key=lambda item: item[1], reverse=True)
        return answer

    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        """Returns listening time of underage family members"""
        total = 0.0

        for session in self.sessions:
            if isinstance(session.user, FamilyMember):
                if session.user.age < age_threshold:
                    total += session.duration_listened_seconds / 60.0
        return total

    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        """Returns top artists sorted by listening time"""
        total = {}

        for session in self.sessions:
            if isinstance(session.track, Song):
                artist = session.track.artist
                if artist not in total:
                    total[artist] = 0.0
                total[artist] += session.duration_listened_seconds / 60.0

        result = []
        for artist, minutes in total.items():
            result.append((artist, minutes))

        result.sort(key=lambda item: item[1], reverse=True)
        return result[:n]

    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        """Returns most listened genre for a user"""
        user = self.get_user(user_id)

        if user is None:
            return None
        if len(user.sessions) == 0:
            return None

        genre_times = {}
        total_seconds = 0

        for session in user.sessions:
            genre = session.track.genre
            if genre not in genre_times:
                genre_times[genre] = 0
            genre_times[genre] += session.duration_listened_seconds
            total_seconds += session.duration_listened_seconds

        best_genre = None
        best_seconds = -1
        for genre, seconds in genre_times.items():
            if seconds > best_seconds:
                best_seconds = seconds
                best_genre = genre

        if total_seconds == 0:
            return None

        percent = best_seconds * 100.0 / total_seconds
        return (best_genre, percent)

    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        """Returns collaborative_playlist with many different artists"""
        coll_playlist = []

        for playlist in self.playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artist_ids = set()
                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artist_ids.add(track.artist.artist_id)
                if len(artist_ids) > threshold:
                    coll_playlist.append(playlist)

        return coll_playlist

    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        """Returns average number of tracks per playlist type"""
        playlist_counts = []
        collaborative_counts = []

        for playlist in self.playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                collaborative_counts.append(len(playlist.tracks))
            else:
                playlist_counts.append(len(playlist.tracks))

        playlist_average = 0.0
        collaborative_average = 0.0

        if len(playlist_counts) > 0:
            playlist_average = sum(playlist_counts) / len(playlist_counts)
        if len(collaborative_counts) > 0:
            collaborative_average = sum(collaborative_counts) / len(collaborative_counts)

        return {
            "Playlist": float(playlist_average),
            "CollaborativePlaylist": float(collaborative_average),
        }

    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        """Returns users who listened all tracks of an album"""
        user_playlist = []

        for user in self.users.values():
            listened_track_ids = set()
            for session in user.sessions:
                listened_track_ids.add(session.track.track_id)

            completed_titles = []
            for album in self.albums.values():
                if len(album.tracks) == 0:
                    continue

                completed = True
                for track in album.tracks:
                    if track.track_id not in listened_track_ids:
                        completed = False
                        break

                if completed:
                    completed_titles.append(album.title)

            if len(completed_titles) > 0:
                user_playlist.append((user, completed_titles))
        return user_playlist