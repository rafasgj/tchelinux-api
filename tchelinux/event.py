"""Events management endpoints."""

from datetime import datetime

from flask import (Blueprint, g, jsonify, request)

from flask_jwt_extended import jwt_required

from haversine import haversine

from sqlalchemy import asc as ascending

from tchelinux.util import (
    administrator_only, extract_fields_from_request, save_object)


event_api = Blueprint("events_api", __name__)


def get_event_dictionary(data):
    """Get event dictionary from SQLAlchemy object."""
    evt = {}
    evt['date'] = data.events.date.strftime("%Y-%m-%d")
    ies_keys = ["name", "address", "latitude", "longitude"]
    ies = {k: getattr(data.institutions, k) for k in ies_keys}
    evt['institution'] = ies
    evt['cname'] = data.cities.cname
    evt['city'] = data.cities.name
    Room = g.db.entity('eventrooms')
    rooms = (g.db.session.query(Room)
             .filter(Room.eventdate == data.events.date)
             .all())
    evt['rooms'] = [{"number": r.number, "topic": r.topic} for r in rooms]
    return evt


def _query_next_events(city=None):
    Event = g.db.entity('events')
    City = g.db.entity('cities')
    Institution = g.db.entity('institutions')
    today = datetime.today()
    q = (g.db.session.query(Event, City, Institution)
         .join(Institution, Institution.id == Event.institution_id)
         .join(City, Institution.city == City.cname))
    if city:
        q = (q
             .filter(Event.institution_id == Institution.id)
             .filter(Institution.city == City.cname)
             .filter((City.cname == city) | (City.name == city)))
    q = q.filter(Event.date >= today)
    return q


@event_api.route('/event', methods=['GET'])
@event_api.route('/event/<city>', methods=['GET'])
def get_next_event(city=None):
    """Retrieve the next event."""
    q = _query_next_events(city)
    Event = g.db.entity('events')
    event = q.order_by(ascending(Event.date)).first()
    if event is None:
        return "No events found.", 204
    else:
        return jsonify(get_event_dictionary(event)), 200


@event_api.route('/event/<lat>/<lon>/<dist>', methods=['GET'])
def get_next_event_closer(lat, lon, dist=150):
    """Retrieve the next event."""
    def closer_than(evt, max_dist):
        a = evt.institutions.latitude
        b = evt.institutions.longitude
        return haversine((float(lat), float(lon)), (a, b)) < (max_dist * 1.1)
    q = _query_next_events()
    Event = g.db.entity('events')
    events = q.order_by(ascending(Event.date)).all()
    events = [e for e in events if closer_than(e, float(dist))]
    return jsonify([get_event_dictionary(e) for e in events]), 200


@event_api.route('/event', methods=['POST'])
@jwt_required
@administrator_only
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

    rooms = fields.get('rooms', 3)
    if type(rooms) == int:
        rooms = [{"number": str(i+1), "topic": "Room {}".format(i+1)}
                 for i in range(rooms)]
    Room = g.db.entity('eventrooms')
    for r in rooms:
        r['eventdate'] = event.date
        room = Room(**r)
        save_object(room)
    return "OK", 201


@event_api.route('/event/<event_date>/rooms', methods=['POST', 'PUT'])
@jwt_required
@administrator_only
def put_configure_event_rooms(event_date):
    """Configure all the rooms for an event."""
    Room = g.db.entity('eventrooms')
    g.db.session.query(Room).filter(Room.eventdate == event_date).delete()
    g.db.session.commit()
    for r in request.json:
        r['eventdate'] = datetime.strptime(event_date, '%Y-%m-%d')
        room = Room(**r)
        save_object(room)
    return "OK", 201


@event_api.route('/events')
def get_events():
    """Retrieve events from the database."""
    result = []
    q = _query_next_events()
    Event = g.db.entity('events')
    events = q.order_by(ascending(Event.date))
    for e in events:
        result.append(get_event_dictionary(e))
    return jsonify(result), 200
