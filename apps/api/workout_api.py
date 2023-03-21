import json
from flask_restful import request

from apps.model.workout import workout_schema, workouts_schema
from apps.shared import db
from apps.core.core_resource import AuthResource
import apps.controller.workout_controller as workout_controller
import apps.controller.exercise_controller as exercise_controller


class WorkoutApi(AuthResource):
    def get(self, workout_id):
        workout = workout_controller.get_workout(workout_id)

        return workout_schema.jsonify(workout)

    def delete(self, workout_id):
        workout_controller.delete_workout(workout_id)
        
        return "Success", 200

class WorkoutListApi(AuthResource):
    def get(self):
        json_filters = request.args.get("filters", None)
        filters = {}
        
        if json_filters is not None:
            filters = json.loads(json_filters)
            
        page = request.args.get("page", None, type=int)
        per_page = request.args.get("per_page", None, type=int)

        order = filters.get("order", None)
        exercise_id = filters.get("exercise_id", None)

        workouts, total = workout_controller.get_paginated_workouts(
            exercise_id=exercise_id,
            page=page,
            per_page=per_page,
            order=order
        )

        response = {
            "items": workouts_schema.dump(workouts),
            "total": total
        }
        
        return response
    
    def post(self):
        workout_controller.set_workout(request.get_json())

        return "Success", 200
