"""Events management endpoints."""

from flask import (g, jsonify, Blueprint)
from datetime import datetime
from sqlalchemy import asc as ascending

from tchelinux.util import (extract_fields_from_request, save_object)


event_api = Blueprint("events_api", __name__)


def get_event_dictionary(event):
    """Get event dictionary from SQLAlchemy object."""
    s = g.db.session
    City = g.db.entity('cities')
    Institution = g.db.entity('institutions')
    evt = {}
    evt['date'] = event.date.strftime("%Y-%m-%d")
    inst = s.query(Institution).filter(Institution.id == event.institution_id)
    inst = inst.one()
    ies = {"name": inst.name, "address": inst.address}
    evt['institution'] = ies
    city = s.query(City).filter(City.cname == inst.city).one()
    evt['cname'] = city.cname
    evt['city'] = city.name
    return evt


@event_api.route('/event', methods=['GET'])
def get_next_event():
    """Retrieve the next event."""
    Event = g.db.entity('events')
    today = datetime.today()
    q = g.db.session.query(Event).filter(Event.date >= today)
    event = q.order_by(ascending(Event.date)).first()
    return jsonify(get_event_dictionary(event)), 200


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
    events = s.query(Event).filter(Event.date >= date)\
        .order_by(ascending(Event.date))
    for e in events:
        result.append(get_event_dictionary(e))
    return jsonify(result), 200
