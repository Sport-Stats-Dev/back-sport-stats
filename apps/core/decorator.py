from flask import g
from flask_restful import request, abort
from functools import wraps

from apps.core.tools import decode_token
from apps.model.user import User
from apps.shared import current_user


def authenticate(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.cookies:
            token = request.cookies['token']
            access_token = decode_token(token, True)

            if access_token is not None:
                g.access_token = access_token
                user = User.query.filter_by(id=access_token['user_id']).first()

                if user is not None:
                    g._current_user = user

        return func(*args, **kwargs)

    return decorated

def auth_requiered(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if current_user is None:
            abort(401) # user isn't logged

        return func(*args, **kwargs)

    return decorated
