from flask import Blueprint, request, jsonify

user_api_blueprint = Blueprint('user_page', __name__, static_folder='static', template_folder='templates')

from apps.api.routes import Routes
from apps.model.user import User, user_schema, users_schema, full_user_schema
from apps.model.exercise import exercises_schema
from apps.shared import db


@user_api_blueprint.route(Routes.USER_ROUTE, methods=['POST'])
def add_user():
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']

    new_user = User(email, username, password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@user_api_blueprint.route(Routes.USER_ROUTE, methods=['GET'])
def get_all_users():
    all_users = User.query.all()

    result = users_schema.dump(all_users)

    return jsonify(result)

@user_api_blueprint.route(Routes.USER_ROUTE + '/<id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get_or_404(id)

    return user_schema.jsonify(user)

@user_api_blueprint.route(Routes.FULL_USER_ROUTE + '/<id>', methods=['GET'])
def get_full_user_by_id(id):
    user = User.query.get_or_404(id)

    return full_user_schema.jsonify(user)

@user_api_blueprint.route(Routes.USER_ROUTE + '/username=<username>', methods=['GET'])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first_or_404()

    return user_schema.jsonify(user)

@user_api_blueprint.route(Routes.USER_ROUTE + '/test/<id>', methods=['GET'])
def get_user_test(id):
    user = User.query.filter_by(id=id).first_or_404()

    print(user.id)
    print(user.username)

    return exercises_schema.jsonify(user.exercises)

@user_api_blueprint.route(Routes.USER_ROUTE + '/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    email = request.json['email']
    username = request.json['username']
    password = request.json['password']

    user.email = email
    user.username = username
    user.password = password

    db.session.commit()

    return user_schema.jsonify(user)

@user_api_blueprint.route(Routes.USER_ROUTE + '/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)
