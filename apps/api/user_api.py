from datetime import datetime
import bcrypt
from flask import jsonify, current_app
from flask_restful import Resource, request, abort

from apps.core.tools import decode_token, make_access_token, make_refresh_token
from apps.model.user import User
from apps.shared import db


class RegisterApi(Resource):
    def post(self):
        payload = request.get_json()

        email = payload.get('email')
        password = payload.get('password')
        
        # TODO: validate email and password
        if email is None or password is None:
            abort(401) # missing arguments
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
        if User.query.filter_by(email=email).first() is not None:
            abort(409) # existing user

        new_user = User(
            email=email,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        
        return 'Success', 200

class LoginApi(Resource):
    def post(self):
        payload = request.get_json()

        email = payload.get('email')
        password = payload.get('password')
    
        if email is None or password is None:
            abort(401) # missing arguments

        user = User.query.filter_by(email=email).first()
        
        if not user:
            abort(401) # unexisting user

        if not bcrypt.checkpw(password.encode('utf-8'), user.password):
            abort(401) # passwords doesn't match

        access_token = make_access_token(user.id)
        refresh_token = make_refresh_token(user.id)

        user.last_connexion = datetime.utcnow()
        user.refresh_token = refresh_token
        db.session.commit()

        response = current_app.make_response(jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }))
        
        return response

class RefreshApi(Resource):
    def post(self):
        payload = request.get_json()
        refresh_token = payload['refresh_token']

        if refresh_token is None:
            abort(401)
        
        decoded_token = decode_token(refresh_token)
        user_id = decoded_token.get('user_id')
        
        if user_id is None:
            abort(401)
        
        user = User.query.filter_by(id=user_id).first()
        if user is None or user.refresh_token != refresh_token:
            abort(401)
        
        access_token = make_access_token(user.id)
        refresh_token = make_refresh_token(user.id)

        user.refresh_token = refresh_token
        db.session.commit()

        response = current_app.make_response(jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }))

        return response
