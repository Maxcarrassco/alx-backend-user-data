#!/usr/bin/usr/env python3
"""Auth Module of User Service."""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Return the hashed of a password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
