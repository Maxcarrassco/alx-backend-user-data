#!/usr/bin/env python3
"""ALX SE Backend Basic Auth Module."""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """Implement all basic auth fynctionalities."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return base64 encoded Basic Auth authorization header value."""
        if not authorization_header or type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Return the decode str of a base64 str."""
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            cred = b64decode(base64_authorization_header)
        except Exception:
            return None
        return cred.decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Return the user credential from the decoded base64 string."""
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        cred = decoded_base64_authorization_header.split(':')
        return cred[0], cred[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Return user instance from user_email and user_pwd or return None."""
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        for user in User.search({'email': user_email}):
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user or None."""
        header = self.authorization_header(request)
        if not header:
            return None
        header64 = self.extract_base64_authorization_header(header)
        if not header64:
            return None
        header_vals = self.decode_base64_authorization_header(header64)
        if not header_vals:
            return None
        user_creds = self.extract_user_credentials(header_vals)
        if not user_creds:
            return None
        user = self.user_object_from_credentials(user_creds[0], user_creds[1])
        return user
