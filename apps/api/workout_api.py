from flask_restful import request

from apps.model.workout import workout_schema, workouts_schema
from apps.core.core_resource import AuthResource
import apps.controller.workout_controller as workout_controller
from apps.shared import current_user


class WorkoutApi(AuthResource):
    def get(self, workout_id):
        workout = workout_controller.get_workout(workout_id)

        return workout_schema.jsonify(workout)

    def delete(self, workout_id):
        workout_controller.delete_workout(workout_id)

        return "Success", 200


class WorkoutListApi(AuthResource):
    def get(self):
        page = request.args.get("page", None, type=int)
        per_page = request.args.get("per_page", None, type=int)

        order = request.args.get("order", None)
        exercise_id = request.args.get("exercise_id", None)

        workouts, total = workout_controller.get_paginated_workouts(
            exercise_id=exercise_id,
            page=page,
            per_page=per_page,
            order=order
        )

        response = {
            "items": workouts_schema.dump(workouts),
            "meta": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": total // per_page + 1,
            }
        }

        return response

    def post(self):
        workout = workout_controller.set_workout(request.get_json())
        return workout_controller.get_workout_details_json(workout.id), 201


class WorkoutDetailsApi(AuthResource):
    def get(self, workout_id):
        return workout_controller.get_workout_details_json(workout_id)


class WorkoutHeatmapApi(AuthResource):
    def get(self):
        response = {
            "data": workout_controller.get_heatmap(),
            "account_creation": current_user.create_date.timestamp()
        }
        return response
