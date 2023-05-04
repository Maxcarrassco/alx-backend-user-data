#!/usr/bin/env python3
"""ALX SE Backend Basic Auth Module"""
from typing import List, Union
from models.user import User
from os import getenv
from flask import request


class Auth:
    """Implement Custom Auth Service."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a route require the user to be authenticated."""
        if not path or not excluded_paths:
            return True
        for e_path in excluded_paths:
            e_len = len(e_path) - 1
            if path[:e_len] == e_path[:e_len] or (
                    path[-1] != '/' and path + '/'[:e_len] == e_path[:e_len]):
                return False
        return True

    def authorization_header(self, request=None) -> Union[str, None]:
        """Return the Authorization header from the request."""
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> Union[User, None]:
        """Return the current user."""
        return None

    def session_cookie(self, request=None) -> Union[str, None]:
        """Return the value of a cookie from request."""
        if not request:
            return None
        cookies = getattr(request, 'cookies', None)
        if not cookies:
            return None
        session_name = getenv('SESSION_NAME')
        return cookies.get(session_name)
