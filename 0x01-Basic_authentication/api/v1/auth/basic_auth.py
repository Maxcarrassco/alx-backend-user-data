#!/usr/bin/env python3
"""ALX SE Backend Basic Auth Module."""
from api.v1.auth.auth import Auth
from base64 import b64decode


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
