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
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    response = make_response(redirect('/'))
    response.set_cookie('session_id', '', expires=0)
    return response


@app.route('/profile', methods=['GET'], strict_slashes=False)
def get_me():
    """Return current user."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return {'email': user.email}, 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Return reset password token."""
    email = request.form.get('email')
    if not email:
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
        return {'email': email, 'reset_token': token}
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_user_password():
    """Reset current user password."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    password = request.form.get('new_password')
    if not (email and reset_token and password):
        abort(403)
    try:
        AUTH.update_password(reset_token, password)
        return {'email': email, 'message': 'Password updated'}
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
