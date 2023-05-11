#!/usr/bin/env python3
"""App Server Module Of User Service."""
from flask import Flask, request, make_response, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """Return home page."""
    return {"message": "Bienvenue"}


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """Register a new user."""
    form = request.form
    try:
        user = AUTH.register_user(form.get('email'), form.get('password'))
        return {'email': user.email, 'message': 'user created'}
    except ValueError:
        return {'message': 'email already registered'}


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login_user():
    """Login a user."""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response({'email': f'{email}', "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout_user():
    """Logout current user."""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    response = make_response(redirect('/'))
    response.set_cookie('session_id', '', expires=0)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
