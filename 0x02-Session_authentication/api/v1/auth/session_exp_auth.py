#!/usr/bin/env python3
"""Session Expire Auth Module."""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from typing import Union
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Implement session auth with expire time."""

    def __init__(self) -> None:
        """Override initialization method of SessionAuth."""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> Union[str, None]:
        """Create a new session."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        created_at = datetime.now()
        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': created_at
                }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> Union[str, None]:
        """Return the session."""
        if not session_id or session_id not in self.user_id_by_session_id:
            return None
        user = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return user['user_id']
        if 'created_at' not in user:
            return None
        if ((user['created_at'] + timedelta(
                seconds=self.session_duration)) < datetime.now()):
            return None
        return user['user_id']
