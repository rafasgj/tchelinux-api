"""User and authentication management endpoints."""

from collections import namedtuple

from flask import (Blueprint, current_app, g, jsonify)

from flask_jwt_extended import (
    create_access_token, get_jwt_identity, jwt_required)

from tchelinux.token import add_token_to_database, revoke_token
from tchelinux.util import (extract_fields_from_request, save_object)


user_api = Blueprint("user_api", __name__)


@user_api.route('/user', methods=['POST'])
def add_user():
    """Add user to the system."""
    errors = []
    fields = extract_fields_from_request(['name', 'email', 'password'], errors)
    if errors:
        return jsonify(errors), 400

    User = g.db.entity('users')
    q = g.db.session.query(User).filter(User.email == fields['email'])
    if q.count() > 0:
        return "Email {} already in use.".format(fields['email']), 400
    user = User(**fields)
    save_object(user)
    return "OK", 201


@user_api.route('/login', methods=['POST'])
def login():
    """Authenticate user in the system."""
    errors = []
    fields = extract_fields_from_request(['email', 'password'], errors)
    if errors:
        return jsonify(errors), 400

    # Identity can be any data that is json serializable
    identity_claim = current_app.config['JWT_IDENTITY_CLAIM']
    # Verify admins ...
    passwd = current_app.config['admin'].get(fields['email'], None)
    if passwd is not None:
        UserProxy = namedtuple("UserProxy", ["email", "password", "role"])
        user = UserProxy(email=fields['email'],
                         password=passwd,
                         role='admin')
    else:
        # ... or users.
        s = g.db.session
        User = g.db.entity('users')
        q = s.query(User).filter(User.email == fields['email'])
        ret = {"error": "Username/Password do not match."}
        if q.count() != 1:
            return jsonify(ret), 401
        else:
            user = q.one()

    if user.password != fields['password']:
        return jsonify(ret), 401

    # TODO: check out how/why use refresh tokens.
    identity = {"username": user.email, "role": user.role}
    access_token = create_access_token(identity=identity)
    # refresh_token = create_refresh_token(identity=identity)

    add_token_to_database(access_token, identity_claim)
    # add_token_to_database(refresh_token, api.config['JWT_IDENTITY_CLAIM'])

    # ret = {"access_token": access_token, "refresh_token": refresh_token}
    ret = {"access_token": access_token}

    return jsonify(ret), 200


@user_api.route('/logout')
@jwt_required
def logout():
    """Terminate user session."""
    user_identity = get_jwt_identity()
    if user_identity is None:
        return jsonify("User not logged in."), 401
    else:
        return revoke_token(user_identity)
