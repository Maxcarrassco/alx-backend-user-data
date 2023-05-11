#!/usr/bin/env python3
"""Auth Module of User Service."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Return the hashed of a password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize the Auth Model."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = str(_hash_password(password))
            return self._db.add_user(email, hashed_password)
        raise ValueError(f'User {email} already exists.')
