"""Entry point for Tchelinux CMS API."""

from flask import (Flask, g)

from tchelinux.database import Database

from tchelinux.city import city_api
from tchelinux.institution import institution_api
from tchelinux.event import event_api


# Configuration
DEBUG = True
SECRET_KEY = 'development key'

# Database Configuration
DATABASE = 'tchelinuxcms'
USERNAME = 'rafael'
PASSWORD = ''


api = Flask(__name__)
api.config.from_object(__name__)

api.register_blueprint(city_api)
api.register_blueprint(institution_api)
api.register_blueprint(event_api)


def connect_db():
    """Connect to the database."""
    if api.testing:
        initstr = "sqlite:///{database}.sqlite"
    else:
        api.config['DATABASE'] = DATABASE
        initstr = "postgres+pg8000://{username}@localhost/{database}"

    initstr = initstr.format(username=USERNAME,
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
