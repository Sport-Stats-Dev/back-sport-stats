from apps.core.core_resource import AuthResource
import apps.controller.training_controller as training_controller


class Average1rmPerTrainingsApi(AuthResource):
    def get(self, exercise_id):
        trainings = training_controller.get_trainings_by_exercise_id(exercise_id)
        average_per_training = []

        for training in trainings:
            average = 0

            for set in training.sets:
                average += get_1rm(set.reps, set.weight)

            average /= len(training.sets.all())

            average_per_training.append({
                "id": training.id,
                "date": str(training.date),
                "value": average
            })

        return average_per_training, 200

def get_1rm(reps: int, weight: int):
    return (weight * reps / 30) + weight
