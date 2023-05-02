#!/usr/bin/env python3
"""ALX SE Backend Basic Auth Module"""
from flask import request, Request
from typing import Union, List, TypeVar

User = TypeVar('User')


class Auth:
    """Implement Custom Basic Auth."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a route require the user to be authenticated."""
        return False

    def authorization_header(self, request: Union[Request, None] = None
                             ) -> Union[str, None]:
        """Return the Authorization header from the request."""
        return None

    def current_user(self, request: Union[Request, None] = None
                     ) -> Union[User, None]:
        """Return the current user."""
        return None
