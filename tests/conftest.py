"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import (
    AlbumTrack,
    SingleRelease,
    InterviewEpisode,
    NarrativeEpisode,
    AudiobookTrack,
)
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


# ---------------------------------------------------------------------------
# Helper - timestamps relative to the real current time so that the
# "last 30 days" window in Q2 always contains RECENT sessions.
# ---------------------------------------------------------------------------


FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)   # well within 30-day window
OLD    = FIXED_NOW - timedelta(days=60)   # outside 30-day window


@pytest.fixture
def platform() -> StreamingPlatform:
    """Return a fully populated StreamingPlatform instance."""
    platform = StreamingPlatform("TestStream")

    # ------------------------------------------------------------------
    # Artists
    # ------------------------------------------------------------------
    pixels  = Artist("a1", "Pixels",    genre="pop")
    rock = Artist("a2", "The Rocks",   genre="rock")
    jazz = Artist("a3", "Jazzers",   genre="jazz")
    classical = Artist("a4", "Beat Makers", genre="electro")

    for artist in (pixels, rock, jazz, classical):
        platform.add_artist(artist)

    # ------------------------------------------------------------------
    # Albums & AlbumTracks
    # ------------------------------------------------------------------
    dd = Album("alb1", "Digital Dreams", artist=pixels, release_year=2022)
    t1 = AlbumTrack("t1", "Pixel Rain",      180, "pop",  pixels, track_number=1)
    t2 = AlbumTrack("t2", "Grid Horizon",    210, "pop",  pixels, track_number=2)
    t3 = AlbumTrack("t3", "Vector Fields",   195, "pop",  pixels, track_number=3)
    for track in (t1, t2, t3):
        dd.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(dd)


    # ------------------------------------------------------------------
    # Additional tracks
    # ------------------------------------------------------------------
    t4 = SingleRelease("t4", "Super rock music", 150, "rock", rock, release_date=date(2024, 1, 2))
    t5 = SingleRelease("t5", "Amazing jazz", 160, "jazz", jazz, release_date=date(2024, 1, 3))
    t6 = SingleRelease("t6", "A track for a bad day", 170, "classical", classical, release_date=date(2024, 1, 4))
    podcast = InterviewEpisode("p1", "Eminem Podcast", 1200, "podcast", host="Eminem", guest="Will Smith")
    narrative = NarrativeEpisode("p2", "Super interesting story", 900, "story", host="Tom Holland", season=1, episode_number=1)
    book = AudiobookTrack("b1", "How to code in python audiobook", 600, "audiobook", author="Jeff Bezos", narrator="Bill Gates")

    for artist, track in ((rock, t4), (jazz, t5), (classical, t6)):
        artist.add_track(track)
        platform.add_track(track)

    for track in (podcast, narrative, book):
        platform.add_track(track)

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    alice = FreeUser("u1", "Alice",   age=30)
    bob   = PremiumUser("u2", "Bob",   age=25, subscription_start=date(2023, 1, 1))
    parent = FamilyAccountUser("u3", "Parent", age=40)
    child1 = FamilyMember("u4", "Child", age=16, parent=parent)
    child2 = FamilyMember("u5", "Child", age=13, parent=parent)

    parent.add_sub_user(child1)
    parent.add_sub_user(child2)

    for user in (alice, bob, parent, child1, child2):
        platform.add_user(user)

    # ------------------------------------------------------------------
    # Playlists
    # ------------------------------------------------------------------
    p1 = Playlist("pl1", "Awesome Music", owner=alice)
    p1.add_track(t1)
    p1.add_track(t4)

    p2 = Playlist("pl2", "Bob's playlist", owner=bob)
    p2.add_track(t2)

    c1 = CollaborativePlaylist("c1", "My bro and I's playlist", owner=bob)
    c1.add_track(t1)
    c1.add_track(t4)
    c1.add_track(t5)
    c1.add_track(t6)

    c2 = CollaborativePlaylist("c2", "Playlist with Eminem", owner=alice)
    c2.add_track(t1)
    c2.add_track(t2)

    for playlist in (p1, p2, c1, c2):
        platform.add_playlist(playlist)

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------
    sessions = [
        ListeningSession("s1", alice, t1, RECENT, 180),
        ListeningSession("s2", alice, t2, OLD, 120),
        ListeningSession("s3", bob, t1, RECENT, 200),
        ListeningSession("s4", bob, t2, RECENT, 220),
        ListeningSession("s5", bob, t2, RECENT + timedelta(minutes=5), 100),
        ListeningSession("s6", bob, t3, RECENT + timedelta(minutes=10), 195),
        ListeningSession("s7", parent, book, RECENT, 300),
        ListeningSession("s8", child1, t3, RECENT, 195),
        ListeningSession("s9", child2, narrative, RECENT + timedelta(minutes=15), 120),
        ListeningSession("s10", parent, t4, RECENT + timedelta(minutes=20), 150),
    ]

    for session in sessions:
        platform.record_session(session)

    return platform


@pytest.fixture
def fixed_now() -> datetime:
    """Expose the shared FIXED_NOW constant to tests."""
    return FIXED_NOW


@pytest.fixture
def recent_ts() -> datetime:
    return RECENT


@pytest.fixture
def old_ts() -> datetime:
    return OLD