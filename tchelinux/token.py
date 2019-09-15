from flask import g, jsonify
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token


def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)


def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.
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
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']
    try:
        Token = g.db.entity('tokens')
        token = g.db.session.query(Token).filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def get_user_tokens(user_identity):
    """
    Returns all of the tokens, revoked and unrevoked, that are stored for the
    given user
    """
    Token = g.db.entity('tokens')
    return (g.db.session.query(Token)
                .filter_by(user_identity=user_identity).all())


def revoke_token(user_identity):
    """
    Revokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
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
    """
    Delete tokens that have expired from the database.

    How (and if) you call this is entirely up you. You could expose it to an
    endpoint that only administrators could call, you could run it as a cron,
    set it up with flask cli, etc.
    """
    now = datetime.now()
    Token = g.db.entity('tokens')
    expired = g.db.session.query(Token).filter(Token.expires < now).all()
    for token in expired:
        g.db.session.delete(token)
    g.db.session.commit()
