"""Utility functions."""


from flask import (g, request)


def orm_as_dict(obj):
    """Create a dictionary from a SQLAlchemy ORM object."""
    from sqlalchemy.inspection import inspect
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def extract_fields_from_request(fields, errors):
    """Get the values of fields from a request."""
    data = request.json
    if not data:
        data = request.form
    for field in fields:
        if data.get(field, None) is None:
            errors.append("'{}' was not provided.".format(field))
    return {k: data[k] for k in data}


def save_object(object):
    """Save object in the current database session."""
    g.db.session.add(object)
    g.db.session.commit()
