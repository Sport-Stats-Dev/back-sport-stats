from flask import jsonify, current_app
from flask_restful import Resource, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from apps.model.user import User, user_schema, users_schema
from apps.shared import db
from apps.core.core_resource import AuthResource


class UserApi(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        
        return user_schema.jsonify(user)

    def post(self):
        payload = request.get_json()

        email = payload['email']
        hashed_password = generate_password_hash(payload['password'], method='sha256')
        
        if email is None or payload['password'] is None:
            abort(401) # missing arguments
            
        if User.query.filter_by(email=email).first() is not None:
            abort(401) # existing user

        new_user = User(email, hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return 'Success', 200

class UserListApi(AuthResource):
    def get(self):
        all_users = User.query.all()

        return jsonify(users_schema.dump(all_users))

class LoginApi(Resource):
    def post(self):
        payload = request.get_json()

        email = payload['email']
        password = payload['password']
    
        if email is None or password is None:
            abort(401) # missing arguments

        user = User.query.filter_by(email=email).first()
        
        if not user:
            abort(401) # unexisting user

        if not check_password_hash(user.password, payload['password']):
            abort(401) # passwords doesn't match

        token = jwt.encode({
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, current_app.config['SECRET_KEY'])
        
        return jsonify({'token' : token})
