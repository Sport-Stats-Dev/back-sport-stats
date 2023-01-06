import json
from flask_restful import request

from apps.core.core_resource import AuthResource
import apps.controller.exercise_controller as exercise_controller
from apps.model.exercise import exercise_schema, exercises_schema


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
        json_filters = request.args.get('filters', None)
        filters = {}
        
        if json_filters is not None:
            filters = json.loads(json_filters)
            
        page = request.args.get('page', None, type=int)
        per_page = request.args.get('per_page', None, type=int)

        order = filters.get('order', None)

        trainings, total = exercise_controller.get_paginated_exercises(
            page=page,
            per_page=per_page,
            order=order
        )

        response = {
            'items': exercises_schema.dump(trainings),
            'total': total
        }
        
        return response

    def post(self):
        payload = request.get_json()
        exercise_controller.set_exercise(payload)
        
        return 'Success', 200
