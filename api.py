"""Entry point for Tchelinux CMS API."""

import json

from flask import (Flask, g)

from flask_jwt_extended import JWTManager

from tchelinux.city import city_api
from tchelinux.database import Database
from tchelinux.event import event_api
from tchelinux.institution import institution_api
from tchelinux.token import is_token_revoked
from tchelinux.user import user_api

api = Flask(__name__)
api.config.from_object(__name__)
with open("apiconfig.json", "r") as cfg:
    api.config.update(json.load(cfg))

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(api)

api.register_blueprint(city_api)
api.register_blueprint(institution_api)
api.register_blueprint(event_api)
api.register_blueprint(user_api)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    """Check if token is revoked."""
    return is_token_revoked(decoded_token)


def connect_db():
    """Connect to the database."""
    if api.testing:
        initstr = "sqlite:///{database}"
    else:
        initstr = "sqlite:///{database}"
        # initstr = "postgres+pg8000://{username}@localhost/{database}"

    initstr = initstr.format(username=api.config['DBUSERNAME'],
                             database=api.config['DATABASE'])
    api_db = Database(initstr)
    try:
        api_db.create()
    except Exception:
        api_db.open()
    return api_db


@api.before_request
def before_request():
    """Execute before each request."""
    g.db = connect_db()


if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=4000)
