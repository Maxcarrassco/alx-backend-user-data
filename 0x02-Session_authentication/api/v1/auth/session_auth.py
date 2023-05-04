#!/usr/bin/env python3
"""ALX SE Backend Custom Session Auth Module."""
from api.v1.auth.auth import Auth
import uuid
from typing import Dict, Union, Any
from models.user import User


class SessionAuth(Auth):
    """This module implement all functionalities of a session auth service."""
    user_id_by_session_id: Dict[str, Any] = {}

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """Create a new user session."""
        if not user_id or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(
            self, session_id: str = None) -> Union[str, None]:
        """Return the user id from session."""
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> Union[User, None]:
        """Return the current user from db using its id from the session"""
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Delete the current user session."""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id or session_id not in self.user_id_by_session_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
