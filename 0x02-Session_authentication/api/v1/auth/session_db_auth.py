#!/usr/bin/env python3
"""Session DB AUth Module."""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from typing import Union
from datetime import datetime, timedelta
from uuid import uuid4
from models.base import DATA


class SessionDBAuth(SessionExpAuth):
    """Implement session based auth that stores it session in json file."""

    def create_session(self, user_id=None) -> Union[str, None]:
        """Create a new session."""
        if not user_id:
            return None
        session_id = str(uuid4())
        if not session_id:
            return None
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> Union[str, None]:
        """Return the user_id from the session from storage."""
        if not session_id:
            return None
        if 'UserSession' not in DATA:
            return None
        session = UserSession.search({'session_id': session_id})
        if not session:
            return None
        session = session[0]
        duration = self.session_duration
        if duration <= 0:
            return session.user_id
        time = datetime.now()
        if (session.created_at + timedelta(seconds=duration)) < time:
            return None
        return session.user_id

    def destroy_session(self, request=None) -> bool:
        """Delete current user session."""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if 'UserSession' not in DATA:
            return False
        session = UserSession.search({'session_id': session_id})
        if not session:
            return False
        session = session[0]
        session.remove()
        return True
