"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

from datetime import date

class User:
    """Base class for all users"""
    def __init__(self, user_id: str, name: str, age: int) -> None:
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session) -> None:
        """Add a listening session to the user"""
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        """Returns total listening time in seconds"""
        total = 0
        for session in self.sessions:
            total += session.duration_listened_seconds
        return total

    def total_listening_minutes(self) -> float:
        """Returns total listening time in minutes"""
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self) -> set[str]:
        """Returns unique tracks listened"""
        answer = set()
        for session in self.sessions:
            answer.add(session.track.track_id)
        return answer

class FreeUser(User):
    """Free tier user with limited features"""
    MAX_SKIPS_PER_HOUR = 6

class PremiumUser(User):
    """Paid subscriber with full access"""
    def __init__(self, user_id: str, name: str, age: int, subscription_start: date) -> None:
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(User):
    """Premium user managing family account"""
    def __init__(self, user_id: str, name: str, age: int) -> None:
        super().__init__(user_id, name, age)
        self.sub_users = []

    def add_sub_user(self, sub_user) -> None:
        """Add a sub-user to the user"""
        if sub_user not in self.sub_users:
            self.sub_users.append(sub_user)
            sub_user.parent = self

    def all_members(self) -> list[User]:
        """Returns all users who are members of this family"""
        return [self] + self.sub_users

class FamilyMember(User):
    """User profile belonging to a family account"""
    def __init__(self, user_id: str, name: str, age: int, parent: FamilyAccountUser) -> None:
        super().__init__(user_id, name, age)
        self.parent = parent