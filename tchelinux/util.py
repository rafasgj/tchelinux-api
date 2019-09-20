"""Utility functions."""

from functools import wraps
from flask import (g, request)
from flask_jwt_extended import get_jwt_identity


def orm_as_dict(obj):
    """Create a dictionary from a SQLAlchemy ORM object."""
    from sqlalchemy.inspection import inspect
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def extract_fields_from_request(required_fields, errors=None):
    """Get the values of fields from a request."""
    data = request.json
    if not data:
        data = request.form
    for field in required_fields:
        if errors is not None and data.get(field, None) is None:
            errors.append("'{}' was not provided.".format(field))
    return {k: data[k] for k in data}


def save_object(object):
    """Save object in the current database session."""
    g.db.session.add(object)
    g.db.session.commit()


def administrator_only(callable):
    """Create a decorator to ensure execution with administrator privileges."""
    @wraps(callable)
    def ensure_admin(*args, **kwargs):
        role = get_jwt_identity().get('role', None)
        if role != 'admin':
            return "Forbidden access.", 403
        else:
            return callable(*args, **kwargs)
    return ensure_admin
