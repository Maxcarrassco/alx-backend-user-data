#!/usr/bin/env python3
"""ALX SE Backend Basic Auth Module"""
from typing import List, TypeVar


class Auth:
    """Implement Custom Basic Auth."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a route require the user to be authenticated."""
        if not path or not excluded_paths:
            return True
        if path in excluded_paths or (
                path[-1] != '/' and path + '/' in excluded_paths):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return the Authorization header from the request."""
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user."""
        return None
