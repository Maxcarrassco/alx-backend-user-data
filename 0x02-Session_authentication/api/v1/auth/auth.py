#!/usr/bin/env python3
"""ALX SE Backend Basic Auth Module"""
from typing import List, TypeVar


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

    def authorization_header(self, request=None) -> str:
        """Return the Authorization header from the request."""
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user."""
        return None
