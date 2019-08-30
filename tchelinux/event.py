"""Events management endpoints."""

from flask import (g, jsonify, Blueprint)

from tchelinux.util import (extract_fields_from_request, save_object)

from datetime import datetime


event_api = Blueprint("events_api", __name__)


@event_api.route('/event', methods=['POST'])
def post_event():
    """Add a new event to the database."""
    errors = []
    fields = extract_fields_from_request(['institution', 'date'], errors)
    if errors:
        return jsonify(errors), 400

    inst = fields['institution']
    Institution = g.db.entity('institutions')
    q = g.db.session.query(Institution)
    f = q.filter(Institution.nick == inst)
    if f.count() > 0:
        institution = f.one()
    else:
        f = q.filter(Institution.name == inst)
        if f.count() == 0:
            return "Institution {} does not exist.".format(inst), 400
        else:
            institution = f.one()
    data = {
        "date": datetime.strptime(fields['date'][:10], '%Y-%m-%d'),
        "institution_id": institution.id
    }

    Event = g.db.entity('events')
    event = Event(**data)
    save_object(event)
    return "OK", 201


@event_api.route('/events', methods=['GET'])
def get_events():
    """Retrieve events from the database."""
    result = []
    date = datetime.today()
    s = g.db.session
    Event = g.db.entity('events')
    City = g.db.entity('cities')
    Institution = g.db.entity('institutions')
    events = s.query(Event).filter(Event.date >= date)
    for e in events:
        evt = {}
        evt['date'] = e.date.strftime("%Y-%m-%d")
        inst = s.query(Institution).filter(Institution.id == e.institution_id)
        inst = inst.one()
        ies = {"name": inst.name, "address": inst.address}
        evt['institution'] = ies
        city = s.query(City).filter(City.cname == inst.city).one()
        evt['cname'] = city.cname
        evt['city'] = city.name
        result.append(evt)
    return jsonify(result), 200
