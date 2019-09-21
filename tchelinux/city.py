"""City management endpoints."""

from flask import (g, jsonify, Blueprint)

from tchelinux.util import (
    orm_as_dict, extract_fields_from_request, save_object, administrator_only)

from flask_jwt_extended import jwt_required


city_api = Blueprint("city_api", __name__)


@city_api.route('/city', methods=['POST'])
@jwt_required
@administrator_only
def post_city():
    """Add a new city to the database."""
    errors = []
    data = extract_fields_from_request(['cname', 'name'], errors)
    if errors:
        return jsonify(errors), 400

    City = g.db.entity('cities')
    city = City(**data)
    save_object(city)
    return "OK", 201


@city_api.route('/cities')
def get_cities():
    """Retrieve a list of all cities."""
    City = g.db.entity('cities')
    cities = g.db.session.query(City)
    return jsonify([orm_as_dict(c) for c in cities]), 200
