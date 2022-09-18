from flask import g
from flask_restful import request, abort
from functools import wraps

from apps.core.tools import decode_token
from apps.model.user import User


def auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_user(False)
        return func(*args, **kwargs)

    return decorated

def auth_requiered(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_user(True)

        return func(*args, **kwargs)

    return decorated

def auth_user(required: bool):
    token = None

    if 'token' in request.cookies:
        token = request.cookies['token']
        access_token = decode_token(token, not required)

        if access_token is not None:
            g.access_token = access_token
            user = User.query.filter_by(id=access_token['user_id']).first()

            if user is None and required:
                abort(401) # user doesn't exist

            if user is not None:
                g._current_user = user

    elif required:
        abort(401) # token is missing
