"""Provides JWT authentication."""

from datetime import datetime

from flask import g, jsonify

from flask_jwt_extended import decode_token

from sqlalchemy.orm.exc import NoResultFound


def _epoch_utc_to_datetime(epoch_utc):
    """Convert epoch timestamps to datetime objects."""
    return datetime.fromtimestamp(epoch_utc)


def add_token_to_database(encoded_token, identity_claim):
    """Add a new token to the database.

    It is not revoked when it is added.
    :param encoded_token:
    :param identity_claim:
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    username = decoded_token[identity_claim]['username']
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = False

    Token = g.db.entity('tokens')
    db_token = Token(
        jti=jti,
        type=token_type,
        username=username,
        expires=expires,
        revoked=revoked,
    )
    g.db.session.add(db_token)
    g.db.session.commit()


def is_token_revoked(decoded_token):
    """Check if the given token is revoked or not."""
    jti = decoded_token['jti']
    try:
        Token = g.db.entity('tokens')
        token = g.db.session.query(Token).filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def get_user_tokens(user_identity):
    """Retrieve all user tokens."""
    Token = g.db.entity('tokens')
    return (g.db.session.query(Token)
                .filter_by(user_identity=user_identity).all())


def revoke_token(user_identity):
    """Revoke the given token."""
    try:
        username = user_identity['username']
        Token = g.db.entity('tokens')
        token = (g.db.session.query(Token)
                 .filter_by(revoked=False, username=username).one())
        token.revoked = True
        g.db.session.commit()
        return "OK", 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


def prune_database():
    """Delete expired and revoked tokens from the database."""
    now = datetime.now()
    Token = g.db.entity('tokens')
    expired = (g.db.session.query(Token)
                   .filter(Token.revoked or Token.expires < now).all())
    for token in expired:
        g.db.session.delete(token)
    g.db.session.commit()
