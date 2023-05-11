#!/usr/bin/env python3
"""App Server Module Of User Service."""
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    """Return home page."""
    return {"message": "Bienvenue"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
