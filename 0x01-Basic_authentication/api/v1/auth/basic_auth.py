#!/usr/bin/env python3
"""ALX SE Backend Basic Auth Module."""
from api.v1.auth.auth import Auth


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
