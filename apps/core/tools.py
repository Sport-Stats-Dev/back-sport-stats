from flask import current_app
from flask_restful import abort
import datetime
import jwt


def refresh_access_token(access_token):
    now = datetime.datetime.utcnow()

    access_token['iat'] = now
    access_token['exp'] = now + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']

    return encode_token(access_token)

def encode_token(payload):
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_token(token, ignore_errors=False):
    access_token = None

    try:
        access_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], "HS256")
    except jwt.exceptions.DecodeError:
        if not ignore_errors: abort(401) # token is invalid
    except jwt.exceptions.ExpiredSignatureError:
        # TODO : renvoyer token expirer pour deco l'user OU date d'expiration sur le cookie de token initial
        if not ignore_errors: abort(401) # token expirated

    return access_token

def add_token_to_response(response, token):
    response.set_cookie('token', token) # TODO: Ajouter httpOnly=True, secure=True (secure à besoin de HTTPS)
