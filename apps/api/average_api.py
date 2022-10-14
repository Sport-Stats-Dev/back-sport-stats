from apps.core.core_resource import AuthResource
import apps.controller.training_controller as training_controller


class Average1rmPerTrainingsApi(AuthResource):
    def get(self, exercise_id):
        return _getData(exercise_id), 200

class EvolutionOf1rmPerTrainingsApi(AuthResource):
    def get(self, exercise_id):
        return _getData(exercise_id, isEvolution=True), 200

def _getData(exercise_id, isEvolution=False):
    trainings = training_controller.get_trainings(exercise_id=exercise_id)
    data = []
    averages = []
    i = 0

    for training in trainings:
        average = 0
        for set in training.sets:
            average += _get_1rm(set.reps, set.weight)
        average /= len(training.sets.all())

        if isEvolution is False:
            value = average
        else:
            averages.append(average)           
            if i == 0:
                value = 0
            else :
                value = ((averages[i] - averages[i - 1]) / averages[i - 1]) * 100
            i += 1

        data.append({
            "id": training.id,
            "date": str(training.date),
            "value": value
        })

    return data

def _get_1rm(reps: int, weight: int):
    return (weight * reps / 30) + weight
