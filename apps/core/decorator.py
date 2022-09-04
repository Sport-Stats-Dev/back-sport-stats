from flask import g, current_app
from flask_restful import request, abort
import jwt
from functools import wraps

from apps.model.user import User


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            abort(401) # token is missing

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], "HS256")
        except jwt.exceptions.DecodeError:
            abort(401) # token is invalid
        except jwt.exceptions.ExpiredSignatureError:
            abort(401) # token expirated

        current_user = User.query.filter_by(id=data['id']).first()

        if current_user is None:
            abort(401) # user doesn't exist

        g.current_user = current_user

        return func(*args, **kwargs)

    return decorated
