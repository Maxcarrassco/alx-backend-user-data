#!/usr/bin/env python3
"""ALX SE Backend user data Module."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Return the hash of a password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
