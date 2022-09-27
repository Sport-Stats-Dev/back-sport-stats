from typing import List
from flask_restful import abort
import datetime

from apps.model.training import Training
from apps.shared import current_user, db
import apps.controller.exercise_controller as exercise_controller
import apps.controller.set_controller as set_controller

def get_training(training_id) -> Training:
    training = Training.query.get_or_404(training_id)

    if training.user_id != current_user.id:
        abort(403) # not user's training

    return training

def get_trainings(exercise_id=None) -> List[Training]:
    queries = [Training.user_id==current_user.id]
        
    if exercise_id is not None:
        queries.append(Training.exercise_id==exercise_id)

    return Training.query.filter(*queries).all()

def delete_training(training_id, commit_database=True):
    training = get_training(training_id)

    for set in training.sets:
        set_controller.delete_set(training_id, set.id, commit_database=False)

    db.session.delete(training)

    if commit_database: 
        db.session.commit()

def format_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
