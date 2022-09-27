from typing import List
from flask_restful import abort
import datetime

from apps.model.training import Training
from apps.shared import current_user
import apps.controller.exercise_controller as exercise_controller

def get_training(training_id) -> Training:
    training = Training.query.get_or_404(training_id)

    if training.user_id != current_user.id:
        abort(403) # not user's training

    return training

def get_trainings_by_exercise_id(exercise_id) -> List[Training]:
    exercise = exercise_controller.get_exercise(exercise_id)

    trainings = Training.query.filter_by(exercise_id=exercise.id).all()

    return trainings

def format_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
