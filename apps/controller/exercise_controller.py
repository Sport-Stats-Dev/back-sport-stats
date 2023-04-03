from typing import List, Tuple
from flask_restful import abort
from apps.model.execution import Execution

from apps.model.exercise import Exercise
from apps.shared import db, current_user
import apps.controller.workout_controller as workout_controller


def get_exercise(exercise_id) -> Exercise:
    exercise = Exercise.query.get_or_404(exercise_id)

    if exercise.user_id != current_user.id:
        abort(403)  # not user's exercise

    return exercise


def get_paginated_exercises(page=None, per_page=None, order=None, name=None) -> Tuple[List[Exercise], int]:
    queries = [Exercise.user_id == current_user.id]

    table = Exercise.query
    sort = Exercise.name.asc()
    splited_order = None
    sort_field = None

    if order is not None:
        splited_order = order.split(".")
        if (splited_order[0] == "execution_count"):
            table = Exercise.query.outerjoin(Execution).group_by(Exercise.id)
            sort_field = db.func.count(Execution.id)
        else:
            sort_field = getattr(Exercise, splited_order[0], None)
        if sort_field is not None:
            if splited_order[1] == "desc":
                sort = sort_field.desc()
            elif splited_order[1] == "asc":
                sort = sort_field.asc()
    
    if name is not None:
        queries.append(Exercise.name.ilike(f"%{name}%"))

    result = table.filter(*queries).order_by(sort).paginate(page=page, per_page=per_page).items
    total = Exercise.query.filter(*queries).count()
    return result, total


def set_exercise(payload, exercise_id=None):
    name = payload["name"]
    description = payload["description"]

    if exercise_id is not None:
        exercise = get_exercise(exercise_id)
        exercise.name = name
        exercise.description = description
    else:
        new_exercise = Exercise(current_user.id, name, description)
        db.session.add(new_exercise)

    db.session.commit()


def delete_exercise(exercise_id):
    exercise = get_exercise(exercise_id)

    for executions in workout_controller.get_executions_by_exercise(exercise_id=exercise_id):
        workout = executions.workout
        workout_controller.delete_execution(executions.id)
        if workout.executions.count() == 0:
            workout_controller.delete_workout(workout.id)

    db.session.delete(exercise)
    db.session.commit()
