#!/usr/bin/env python3
"""User Service Module."""
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Sqlachemy Base Model."""
    pass


class User(Base):
    """User Model."""
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(250), nullable=False)
    session_id: Mapped[str] = mapped_column(String(250))
    reset_token: Mapped[str] = mapped_column(String(250))
