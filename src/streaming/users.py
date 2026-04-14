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
    def __init__(self, user_id: str, name: str, age: int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def total_listening_seconds(self):
        total = 0
        for session in self.sessions:
            total += session.duration_listened_seconds
        return total

    def total_listening_minutes(self):
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self):
        answer = set()
        for session in self.sessions:
            answer.add(session.track.track_id)
        return answer

class FreeUser(User):
    """Free tier user with limited features"""
    MAX_SKIPS_PER_HOUR = 6

class PremiumUser(User):
    """Paid subscriber with full access"""
    def __init__(self, user_id: str, name: str, age: int, subscription_start: date):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(PremiumUser):
    """Premium user managing family account"""
    def __init__(self, user_id: str, name: str, age: int, subscription_start=None):
        if subscription_start is None:
            subscription_start = date.today()
        super().__init__(user_id, name, age, subscription_start)
        self.sub_users = []

    def add_sub_user(self, sub_user):
        if sub_user not in self.sub_users:
            self.sub_users.append(sub_user)
            sub_user.parent = self

    def all_members(self):
        return [self] + self.sub_users

class FamilyMember(User):
    """User profile belonging to a family account"""
    def __init__(self, user_id: str, name: str, age: int, parent=None):
        super().__init__(user_id, name, age)
        self.parent = parent