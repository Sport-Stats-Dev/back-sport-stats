import json
from flask_restful import request

from apps.core.core_resource import AuthResource
from apps.controller import exercise_controller, training_controller
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

class ExerciseDetailsApi(AuthResource):
    def get(self, exercise_id):
        exercise = exercise_controller.get_exercise(exercise_id)
        last_training = training_controller.get_last_training(exercise_id=exercise_id)

        details = {}
        if last_training:
            best_one_rm_training = training_controller.get_best_one_rm_training(exercise_id=exercise_id)
            best_volume_training = training_controller.get_best_volume_training(exercise_id=exercise_id)

            details['last_training_date'] = str(last_training.date) 
            details['last_training_id'] = last_training.id
            details['best_one_rm'] = best_one_rm_training.get_one_rm_average()
            details['best_one_rm_id'] = best_one_rm_training.id
            details['best_volume'] = best_volume_training.get_volume()
            details['best_volume_id'] = best_volume_training.id

        return { 'exercise': exercise_schema.dump(exercise), 'details': details }
