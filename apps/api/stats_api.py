from flask_restful import request

from datetime import datetime
from apps.core.core_resource import AuthResource
import apps.controller.workout_controller as workout_controller
from apps.model.execution import Execution


class OneRmsApi(AuthResource):
    def get(self, exercise_id):
        return _get_data(exercise_id, Execution.get_one_rm_average), 200


class OneRmsEvolApi(AuthResource):
    def get(self, exercise_id):
        return _get_data(exercise_id, Execution.get_one_rm_average, isEvolution=True), 200

class VolumesApi(AuthResource):
    def get(self, exercise_id):
        return _get_data(exercise_id, Execution.get_volume), 200


class VolumesEvolApi(AuthResource):
    def get(self, exercise_id):
        return _get_data(exercise_id, Execution.get_volume, isEvolution=True), 200


class MaxWeightApi(AuthResource):
    def get(self, exercise_id):
        return _get_data(exercise_id, Execution.get_max_weight), 200


def _get_data(exercise_id, func, isEvolution=False):
    periodStart = request.args.get("periodStart", None, type=int)
    executions = workout_controller.get_executions_by_exercise(exercise_id=exercise_id, periodStart=periodStart)
    data = []
    average = None

    for e in executions:
        if isEvolution:
            value = ((func(e) - average) / average) * 100 if average is not None else 0
            average = func(e)
        else:
            value = func(e)

        data.append({
            "execution_id": e.id,
            "date": datetime.timestamp(e.workout.date),
            "value": value
        })

        data.sort(key=lambda x: x["date"])

    return data
