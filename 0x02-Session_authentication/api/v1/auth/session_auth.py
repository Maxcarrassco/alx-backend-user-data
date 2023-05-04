#!/usr/bin/env python3
"""ALX SE Backend Custom Session Auth Module."""
from api.v1.auth.auth import Auth
import uuid
from typing import Dict, Union


class SessionAuth(Auth):
    """This module implement all functionalities of a session auth service."""
    user_id_by_session_id: Dict[str, str] = {}

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
