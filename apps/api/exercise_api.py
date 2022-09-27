from flask_restful import request

from apps.shared import current_user
from apps.core.core_resource import AuthResource
import apps.controller.exercise_controller as exercise_controller
from apps.model.exercise import Exercise, exercise_schema, exercises_schema


class ExerciseApi(AuthResource):
    def get(self, exercise_id):
        exercise = exercise_controller.get_exercise(exercise_id)

        return exercise_schema.jsonify(exercise)

    def put(self, exercise_id):
        payload = request.get_json()
        exercise_controller.set_exercise(payload, exercise_id)

        return 'Success', 200

    def delete(self, exercise_id):
        exercise_controller.delete_exercise(exercise_id)

        return 'Success', 200

class ExerciseListApi(AuthResource):
    def get(self):
        exercises = Exercise.query.filter_by(user_id=current_user.id).all()
        
        return exercises_schema.dump(exercises)

    def post(self):
        payload = request.get_json()
        exercise_controller.set_exercise(payload)
        
        return 'Success', 200
