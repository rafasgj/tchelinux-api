"""Institution Endpoints."""

from flask import (g, jsonify, Blueprint)
from tchelinux.util import (
    orm_as_dict, extract_fields_from_request, save_object, administrator_only)
from flask_jwt_extended import jwt_required


institution_api = Blueprint("institution_api", __name__)


@institution_api.route('/institution', methods=['POST'])
@jwt_required
@administrator_only
def post_institution():
    """Retrieve a list of all cities."""
    errors = []
    fields = ['name', 'nick', 'city', 'address']
    data = extract_fields_from_request(fields, errors)

    City = g.db.entity('cities')
    try:
        g.db.session.query(City).filter(City.cname == data['city']).one()
    except Exception:
        errors.append("City '{}' do not exist.".format(data['city']))

    if errors:
        return jsonify(errors), 400

    Institution = g.db.entity('institutions')
    inst = Institution(**data)
    save_object(inst)
    return "OK", 201


@institution_api.route('/institution/<string:city>', methods=['GET'])
def get_institutions(city):
    """Retrieve all institutions in a given city."""
    Institution = g.db.entity('institutions')
    q = g.db.session.query(Institution)
    f = q.filter(Institution.city == city)
    if f.count() > 0:
        return jsonify([orm_as_dict(i) for i in q]), 200
    else:
        City = g.db.entity('cities')
        cities = g.db.session.query(City).filter(City.name == city).one()
        city = cities.cname
        f = q.filter(Institution.city == city)
        if q.count() > 0:
            return jsonify([orm_as_dict(i) for i in q]), 200
        else:
            return "No cities found.", 204
