from typing import List, Tuple
from flask_restful import abort
import datetime

from apps.model.training import Training
from apps.shared import current_user, db
import apps.controller.set_controller as set_controller
import apps.controller.exercise_controller as exercise_controller

def get_training(training_id) -> Training:
    training = Training.query.get_or_404(training_id)

    if training.user_id != current_user.id:
        abort(403) # not user's training

    return training

def get_trainings(exercise_id=None) -> List[Training]:
    queries = _get_queries(exercise_id=exercise_id)
    
    return Training.query.filter(*queries).all()

def get_paginated_trainings(exercise_id=None, page=None, per_page=None, order=None) -> Tuple[List[Training], int]:
    queries = _get_queries(exercise_id=exercise_id)

    sort = Training.date.desc()
    splited_order = None
    sort_field = None

    if order is not None:
        splited_order = order.split('.')
        sort_field = getattr(Training, splited_order[0], None)
        if sort_field is not None:
            if splited_order[1] == 'desc':
                sort = sort_field.desc()
            elif splited_order[1] == 'asc':
                sort = sort_field.asc()

    result = Training.query.filter(*queries).order_by(sort).paginate(page=page, per_page=per_page).items
    total = Training.query.filter(*queries).count()
    return result, total

def delete_training(training_id, commit_database=True):
    training = get_training(training_id)
    exercise = exercise_controller.get_exercise(training.exercise_id)

    for set in training.sets:
        set_controller.delete_set(training_id, set.id, commit_database=False)

    exercise.training_count -= 1
    db.session.delete(training)

    if commit_database: 
        db.session.commit()

def format_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

def _get_queries(exercise_id=None):
    queries = [Training.user_id==current_user.id]
        
    if exercise_id is not None:
        queries.append(Training.exercise_id==exercise_id)

    return queries
