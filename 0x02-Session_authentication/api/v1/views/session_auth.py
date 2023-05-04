#!/usr/bin/env python3
"""Session Auth View Module."""
from api.v1.views import app_views
from flask import request, make_response
from typing import Tuple
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user_view() -> str:
    """Generate and set the user session id."""
    email = request.form.get('email')
    if not email:
        return {'error': 'email missing'}, 400
    password = request.form.get('password')
    if not password:
        return {'error': 'password missing'}, 400
    users = User.search({'email': email})
    for i, user in enumerate(users):
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            session_name = getenv('SESSION_NAME')
            res = make_response(user.to_json())
            res.set_cookie(session_name, session_id)
            return res
        if i == len(users) - 1:
            return {'error': 'wrong password'}, 401
    return {'error': 'no user found for this email'}, 404
