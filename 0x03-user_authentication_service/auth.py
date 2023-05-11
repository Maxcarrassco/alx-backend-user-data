#!/usr/bin/env python3
"""Auth Module of User Service."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Return the hashed of a password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


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
            hashed_password = _hash_password(password).decode('utf-8')
            return self._db.add_user(email, hashed_password)
        raise ValueError(f'User {email} already exists.')

    def valid_login(self, email: str, password: str) -> bool:
        """Return True if user credential is valid or False otherwise."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password.encode('utf-8'))
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """Return a uuid4 in a string form."""
        return str(uuid4())

    def create_session(self, email: str) -> Union[str, None]:
        """Create a new session for an user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get a user from db using the user session_id."""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Reset user session_id to None in the database."""
        try:
            self._db.update_user(id=user_id, session_id=None)
        except Exception:
            return None
