from apps.core.core_resource import AuthResource
import apps.controller.training_controller as training_controller
from apps.model.training import Training


class OneRmsApi(AuthResource):
    def get(self, exercise_id):
        return _get_data(exercise_id, Training.get_one_rm_average), 200


class OneRmsEvolApi(AuthResource):
    def get(self, exercise_id):
        return _get_data(exercise_id, Training.get_one_rm_average, isEvolution=True), 200

class VolumesApi(AuthResource):
    def get(self, exercise_id):
        return _get_data(exercise_id, Training.get_volume), 200


class VolumesEvolApi(AuthResource):
    def get(self, exercise_id):
        return _get_data(exercise_id, Training.get_volume, isEvolution=True), 200


def _get_data(exercise_id, func, isEvolution=False):
    trainings = training_controller.get_trainings(exercise_id=exercise_id)
    data = []
    average = None

    for training in trainings:
        if isEvolution:
            value = ((func(training) - average) / average) * 100 if average is not None else 0
            average = func(training)
        else:
            value = func(training)

        data.append({
            "id": training.id,
            "date": str(training.date),
            "value": value
        })

    return data
