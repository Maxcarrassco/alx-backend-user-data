#!/usr/bin/env python3
"""App Server Module Of User Service."""
from flask import Flask, request, make_response
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
