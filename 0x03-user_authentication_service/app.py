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
    form = request.form
    if not AUTH.valid_login(form.get('email'), form.get('password')):
        abort(401)
    email = form.get('email')
    session_id = AUTH.create_session(form.get('email'))
    response = make_response({'email': f'{email}', "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
