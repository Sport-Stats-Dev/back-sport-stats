from flask import Blueprint, request, jsonify

exercise_blueprint = Blueprint('exercise_blueprint', __name__, static_folder='static', template_folder='templates')

from apps.api.routes import Routes
from apps.model.exercise import Exercise, exercise_schema, exercises_schema
from apps.shared import db

import datetime


@exercise_blueprint.route(Routes.EXERCISE_ROUTE, methods=['POST'])
def add_exercise():
    user_id = request.json['user_id']
    date = datetime.datetime.strptime(request.json['date'], '%Y-%m-%dT%H:%M:%S')
    feeling = request.json['feeling']
    comment = request.json['comment']

    new_exercise = Exercise(user_id, date, feeling, comment)

    db.session.add(new_exercise)
    db.session.commit()

    return exercise_schema.jsonify(new_exercise)

@exercise_blueprint.route(Routes.EXERCISE_ROUTE, methods=['GET'])
def get_all_exercise():
    return jsonify(exercises_schema.dump(Exercise.query.all()))

@exercise_blueprint.route(Routes.EXERCISE_ROUTE + '/<id>', methods=['GET'])
def get_exercise_by_id(id):
    return exercise_schema.jsonify(Exercise.query.get_or_404(id))

@exercise_blueprint.route(Routes.EXERCISE_ROUTE + '/user_id=<user_id>', methods=['GET'])
def get_exercise_by_user_id(user_id):
    return exercise_schema.jsonify(Exercise.query.filter_by(user_id=user_id).first_or_404())

@exercise_blueprint.route(Routes.EXERCISE_ROUTE + '/<id>', methods=['PUT'])
def update_exercise(id):
    exercise = Exercise.query.get(id)

    date = request.json['date']
    feeling = request.json['feeling']
    comment = request.json['comment']

    exercise.date = date
    exercise.feeling = feeling
    exercise.comment = comment

    db.session.commit()

    return exercise_schema.jsonify(exercise)

@exercise_blueprint.route(Routes.EXERCISE_ROUTE + '/<id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)

    db.session.delete(exercise)
    db.session.commit()

    return exercise_schema.jsonify(exercise)
