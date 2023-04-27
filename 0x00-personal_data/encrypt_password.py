#!/usr/bin/env python3
"""ALX SE Backend user data Module."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Return the hash of a password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the plain password is equivalent to the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
