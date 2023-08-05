import json
from flask_restful import request

from apps.core.core_resource import AuthResource
from apps.controller import exercise_controller, workout_controller
from apps.model.exercise import exercise_schema, exercises_schema
from apps.model.execution import execution_schema


class ExerciseApi(AuthResource):
    def get(self, exercise_id):
        exercise = exercise_controller.get_exercise(exercise_id)

        return exercise_schema.jsonify(exercise)

    def put(self, exercise_id):
        payload = request.get_json()
        exercise_controller.set_exercise(payload, exercise_id)

        return "Success", 200

    def delete(self, exercise_id):
        exercise_controller.delete_exercise(exercise_id)

        return "Success", 200

class ExerciseListApi(AuthResource):
    def get(self):
        json_filters = request.args.get("filters", None)
        filters = {}
        
        if json_filters is not None:
            filters = json.loads(json_filters)
            
        page = request.args.get("page", None, type=int)
        per_page = request.args.get("per_page", None, type=int)

        order = filters.get("order", None)
        name = filters.get("name", None)

        exercises, total = exercise_controller.get_paginated_exercises(
            page=page,
            per_page=per_page,
            order=order,
            name=name
        )

        response = {
            "items": exercises_schema.dump(exercises),
            "total": total
        }

        for exercise in response["items"]:
            exercise["execution_count"] = workout_controller.get_executions_count_by_exercise(exercise_id=exercise["id"])
        
        return response

    def post(self):
        payload = request.get_json()
        exercise_controller.set_exercise(payload)
        
        return "Success", 200

class ExerciseDetailsApi(AuthResource):
    def get(self, exercise_id):
        exercise = exercise_controller.get_exercise(exercise_id)

        details = {}
        details["execution_count"] = workout_controller.get_executions_count_by_exercise(exercise_id=exercise_id)
        
        if details["execution_count"] > 0:
            last = workout_controller.get_last_execution(exercise_id=exercise_id)
            best_one_rm = workout_controller.get_best_one_rm_execution(exercise_id=exercise_id)
            best_volume = workout_controller.get_best_volume_execution(exercise_id=exercise_id)

            details["last_workout_date"] = str(last.workout.date) 
            details["last_workout_id"] = last.id
            details["best_one_rm"] = best_one_rm.get_one_rm_average()
            details["best_one_rm_id"] = best_one_rm.id
            details["best_volume"] = best_volume.get_volume()
            details["best_volume_id"] = best_volume.id

        return { "exercise": exercise_schema.dump(exercise), "details": details }

class ExerciseLastExecutionApi(AuthResource):
    def get(self, exercise_id):
        execution = workout_controller.get_last_execution(exercise_id=exercise_id)
        return execution_schema.dump(execution) if execution else None
