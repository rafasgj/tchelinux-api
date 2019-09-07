"""User and authentication management endpoints."""

from flask import (g, jsonify, Blueprint)
from tchelinux.util import (extract_fields_from_request, save_object)

from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)


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

    s = g.db.session
    User = g.db.entity('users')
    q = s.query(User).filter(User.email == fields['email'])
    if q.count() != 1:
        return "Username/Password do not match.", 400
    else:
        user = q.one()
        if user.password != fields['password']:
            return "Username/Password do not match.", 400

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity={"role": user.role})
    return jsonify(access_token=access_token), 200


@user_api.route('/logout')
@jwt_required
def logout():
    """Terminate user session."""
    # TODO: Actually implement blacklisting identities.
    role = get_jwt_identity().get('role', None)
    if role is None:
        return jsonify("User not logged in."), 401
    else:
        return jsonify("OK"), 200
