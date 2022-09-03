from flask import jsonify
from flask_restful import Resource, request

from apps.model.user import User, user_schema, users_schema
from apps.shared import db

class UserApi(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        
        return user_schema.jsonify(user)

    def post(self):
        payload = request.get_json()

        new_user = User(payload['email'], payload['password'])

        db.session.add(new_user)
        db.session.commit()
        
        return 'Success', 200

class UserListApi(Resource):
    def get(self):
        all_users = User.query.all()

        return jsonify(users_schema.dump(all_users))