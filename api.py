"""Entry point for Tchelinux CMS API."""

from flask import (Flask, g)

from tchelinux.database import Database

from tchelinux.city import city_api
from tchelinux.institution import institution_api
from tchelinux.event import event_api
from tchelinux.user import user_api

from flask_jwt_extended import JWTManager


api = Flask(__name__)
api.config.from_object(__name__)

# These should got into a unversioned configuration file.
configuration = {
    'JWT_SECRET_KEY': 'super-secret',
    'DBUSERNAME': 'somebody',
    'DATABASE': 'tchelinuxcms',
}
for k, v in configuration.items():
    api.config[k] = v
# /end of configuration

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(api)

api.register_blueprint(city_api)
api.register_blueprint(institution_api)
api.register_blueprint(event_api)
api.register_blueprint(user_api)


def connect_db():
    """Connect to the database."""
    if api.testing:
        initstr = "sqlite:///{database}.sqlite"
    else:
        initstr = "sqlite:///{database}.sqlite"
        # api.config['DATABASE'] = DATABASE
        # initstr = "postgres+pg8000://{username}@localhost/{database}"

    initstr = initstr.format(username=api.config['DBUSERNAME'],
                             database=api.config['DATABASE'])
    db = Database(initstr)
    try:
        db.create()
    except Exception as ex:
        db.open()
    return db


@api.before_request
def before_request():
    """Execute before each request."""
    g.db = connect_db()


if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=4000)
