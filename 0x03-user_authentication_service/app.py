#!/usr/bin/env python3
"""App Server Module Of User Service."""
from flask import Flask, request
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
