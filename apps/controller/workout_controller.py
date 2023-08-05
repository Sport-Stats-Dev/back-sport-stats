from typing import List, Tuple
from flask_restful import abort
from datetime import datetime

from apps.model.execution import Execution
from apps.model.set import Set
from apps.model.workout import Workout
from apps.shared import current_user, db
from apps.controller import exercise_controller


def get_workout(workout_id) -> Workout:
    workout = Workout.query.get_or_404(workout_id)

    if workout.user_id != current_user.id:
        abort(403)  # not user's workout

    return workout


def get_last_execution(exercise_id=None) -> Execution:
    queries = _get_queries()
    queries.append(Execution.exercise_id == exercise_id)
    return Execution.query.join(Workout).filter(*queries).order_by(Workout.date.desc()).first()


def get_execution(execution_id) -> Execution:
    queries = _get_queries()
    queries.append(Execution.id == execution_id)
    return Execution.query.join(Workout).filter(*queries).first()


def get_best_one_rm_execution(exercise_id=None) -> Execution:
    queries = _get_queries()
    queries.append(Execution.exercise_id == exercise_id)
    executions = Execution.query.join(Workout).filter(*queries).all()

    best_one_rm = 0
    best_execution = None

    for execution in executions:
        one_rm = execution.get_one_rm_average()
        if one_rm > best_one_rm:
            best_one_rm = one_rm
            best_execution = execution

    return best_execution


def get_best_volume_execution(exercise_id=None) -> Execution:
    queries = _get_queries()
    queries.append(Execution.exercise_id == exercise_id)
    executions = Execution.query.join(Workout).filter(*queries).all()

    best_volume = 0
    best_execution = None

    for execution in executions:
        volume = execution.get_volume()
        if volume > best_volume:
            best_volume = volume
            best_execution = execution

    return best_execution


def get_workouts(exercise_id=None) -> List[Workout]:
    queries = _get_queries(exercise_id=exercise_id)
    return Workout.query.filter(*queries).all()


def get_paginated_workouts(exercise_id=None, page=None, per_page=None, order=None) -> Tuple[List[Workout], int]:
    queries = _get_queries(exercise_id=exercise_id)

    sort = Workout.date.desc()
    splited_order = None
    sort_field = None

    if order is not None:
        splited_order = order.split(".")
        sort_field = getattr(Workout, splited_order[0], None)
        if sort_field is not None:
            if splited_order[1] == "desc":
                sort = sort_field.desc()
            elif splited_order[1] == "asc":
                sort = sort_field.asc()

    result = Workout.query.filter(*queries).order_by(sort).paginate(page=page, per_page=per_page).items
    total = Workout.query.filter(*queries).count()
    return result, total


def set_workout(payload):
    workout = Workout(
        user_id=current_user.id,
        name=payload["name"],
        date=datetime.fromtimestamp(payload["date"]),
        duration=payload["duration"],
        notes=payload["notes"] if "notes" in payload else None
    )
    for e in payload["executions"]:
        execution = Execution(
            exercise_id=e["exercise_id"],
            order=e["order"],
            notes=e["notes"] if "notes" in e else None
        )
        workout.executions.append(execution)
        for s in e["sets"]:
            execution.sets.append(Set(
                order=s["order"],
                weight=s["weight"],
                reps=s["reps"]
            ))

    db.session.add(workout)
    db.session.commit()


def delete_workout(workout_id):
    db.session.delete(get_workout(workout_id))
    db.session.commit()


def delete_execution(execution_id):
    db.session.delete(get_execution(execution_id))
    db.session.commit()


def get_executions_by_exercise(exercise_id, periodStart=None, periodEnd=None):
    periodFilters = []
    if periodStart is not None:
        periodFilters.append(Workout.date >= datetime.fromtimestamp(periodStart))
    if periodEnd is not None:
        periodFilters.append(Workout.date <= datetime.fromtimestamp(periodEnd))

    return Execution.query.join(Workout).filter(
        Workout.user_id == current_user.id,
        Execution.exercise_id == exercise_id,
        *periodFilters
    ).all()


def get_executions_count_by_exercise(exercise_id):
    return Execution.query.join(Workout).filter(Workout.user_id == current_user.id, Execution.exercise_id == exercise_id).count()


def _get_queries(exercise_id=None):
    queries = [Workout.user_id == current_user.id]

    if exercise_id is not None:
        exercise_controller.get_exercise(exercise_id)
        queries.append(Workout.executions.any(
            Execution.exercise_id == exercise_id))

    return queries
