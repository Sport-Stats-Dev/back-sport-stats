from flask import current_app
from flask_restful import abort
import datetime
import jwt


def make_access_token(user_id: str) -> str:
    now = datetime.datetime.utcnow()
    access_token = {
        'user_id': user_id
    }
    access_token['iat'] = now
    access_token['exp'] = now + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']

    return encode_token(access_token)

def make_refresh_token(user_id: str) -> str:
    now = datetime.datetime.utcnow()
    refresh_token = {
        'user_id': user_id
    }
    refresh_token['iat'] = now
    refresh_token['exp'] = now + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']

    return encode_token(refresh_token)

def encode_token(payload) -> str:
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_token(token, ignore_errors=False) -> dict:
    try:
        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], "HS256")
    except jwt.exceptions.DecodeError:
        if not ignore_errors: abort(401) # token is invalid
    except jwt.exceptions.ExpiredSignatureError:
        if not ignore_errors: abort(401) # token expirated

    return decoded_token
