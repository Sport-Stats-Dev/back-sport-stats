from flask import Blueprint, request, jsonify

user_blueprint = Blueprint('user_page', __name__, static_folder='static', template_folder='templates')

from api.routes import Routes
from model.user import User, users_schema, user_schema
from main import db


@user_blueprint.route(Routes.USER_ROUTE, methods=['POST'])
def add_user():
  username = request.json['username']
  password = request.json['password']

  new_user = User(username, password)

  db.session.add(new_user)
  db.session.commit()

  return user_schema.jsonify(new_user)

@user_blueprint.route(Routes.USER_ROUTE, methods=['GET'])
def get_all_users():
  all_products = User.query.all()
  
  result = users_schema.dump(all_products)

  return jsonify(result)

@user_blueprint.route(Routes.USER_ROUTE + '/<id>', methods=['GET'])
def get_user(id):
  user = User.query.get_or_404(id)

  return user_schema.jsonify(user)

@user_blueprint.route(Routes.USER_ROUTE + '/<id>', methods=['PUT'])
def update_user(id):
  user = User.query.get(id)

  username = request.json['username']
  password = request.json['password']

  user.username = username
  user.password = password

  db.session.commit()

  return user_schema.jsonify(user)

@user_blueprint.route(Routes.USER_ROUTE + '/<id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.get(id)

  db.session.delete(user)
  db.session.commit()

  return user_schema.jsonify(user)
