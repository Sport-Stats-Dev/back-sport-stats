from typing import List, Tuple
from flask_restful import abort
from datetime import datetime

from apps.model.execution import Execution, execution_schema
from apps.model.set import Set
from apps.model.workout import Workout, workout_schema
from apps.shared import current_user, db
from apps.controller import exercise_controller


def get_workout(workout_id) -> Workout:
    workout = Workout.query.get_or_404(workout_id)

    if workout.user_id != current_user.id:
        abort(403)  # not user's workout

    return workout


def get_last_execution(exercise_id=None, before_date=None) -> Execution:
    queries = _get_queries()
    queries.append(Execution.exercise_id == exercise_id)
    if before_date is not None:
        queries.append(Workout.date < before_date)
    return Execution.query.join(Workout).filter(*queries).order_by(Workout.date.desc()).first()


def get_previous_executions(workout: Workout) -> List[Execution]:
    past_executions = []

    for execution in workout.executions:
        past_execution = get_last_execution(exercise_id=execution.exercise_id, before_date=workout.date)
        if past_execution is not None:
            past_executions.append(past_execution)

    return past_executions


def get_paginated_exercise_executions(exercise_id=None, page=None, per_page=None) -> Tuple[List[Execution], int]:
    queries = _get_queries(exercise_id=exercise_id)

    sort = Workout.date.desc()

    result = Execution.query.join(Workout).filter(*queries).order_by(sort).paginate(page=page, per_page=per_page).items
    total = Execution.query.join(Workout).filter(*queries).count()
    return result, total


def get_execution(execution_id) -> Execution:
    queries = _get_queries()
    queries.append(Execution.id == execution_id)
    return Execution.query.join(Workout).filter(*queries).first()


def get_best_one_rm_execution(exercise_id, offset=0) -> Execution:
    queries = _get_queries()
    queries.append(Execution.exercise_id == exercise_id)
    executions = Execution.query.join(Workout).filter(*queries).all()

    best_execution = None

    executions.sort(key=lambda x: x.get_one_rm_average(), reverse=True)
    if len(executions) - offset > 0:
        best_execution = executions[offset]

    return best_execution


def get_best_volume_execution(exercise_id, offset=0) -> Execution:
    queries = _get_queries()
    queries.append(Execution.exercise_id == exercise_id)
    executions = Execution.query.join(Workout).filter(*queries).all()

    best_execution = None

    executions.sort(key=lambda x: x.get_volume(), reverse=True)
    if len(executions) - offset > 0:
        best_execution = executions[0]

    return best_execution


def get_record_one_rm_set(exercise_id, offset=0) -> Set:
    queries = _get_queries()
    queries.append(Execution.exercise_id == exercise_id)
    executions = Execution.query.join(Workout).filter(*queries).order_by(Workout.date.asc()).all()
    best_set_execution = None

    unique_one_rms = {}
    unique_executions = []
    for e in executions:
        one_rm = e.get_best_set_one_rm_value()
        if one_rm not in unique_one_rms:
            unique_one_rms[one_rm] = True
            unique_executions.append(e)

    unique_executions.sort(key=lambda x: x.get_best_set_one_rm_value(), reverse=True)

    if len(unique_executions) - offset > 0:
        best_set_execution = unique_executions[offset]

    best_set = None
    if best_set_execution is not None:
        best_set = best_set_execution.get_best_set_one_rm()

    return best_set


def get_record_volume_set(exercise_id, offset=0) -> Set:
    queries = _get_queries()
    queries.append(Execution.exercise_id == exercise_id)
    executions = Execution.query.join(Workout).filter(*queries).order_by(Workout.date.asc()).all()
    best_set_execution = None

    unique_volumes = {}
    unique_executions = []
    for e in executions:
        volume = e.get_best_set_volume_value()
        if volume not in unique_volumes:
            unique_volumes[volume] = True
            unique_executions.append(e)

    unique_executions.sort(key=lambda x: x.get_best_set_volume_value(), reverse=True)

    if len(unique_executions) - offset > 0:
        best_set_execution = unique_executions[offset]

    best_set = None
    if best_set_execution is not None:
        best_set = best_set_execution.get_best_set_one_rm()

    return best_set


def get_best_volume_workout(offset=0) -> Workout:
    queries = _get_queries()
    workouts = Workout.query.filter(*queries).order_by(Workout.date.asc()).all()
    best_workout = None

    unique_volumes = {}
    unique_workouts = []
    for w in workouts:
        volume = w.get_volume()
        if volume not in unique_volumes:
            unique_volumes[volume] = True
            unique_workouts.append(w)

    unique_workouts.sort(key=lambda x: x.get_volume(), reverse=True)

    if len(unique_workouts) - offset > 0:
        best_workout = unique_workouts[offset]

    return best_workout


def get_workouts(exercise_id=None) -> List[Workout]:
    queries = _get_queries(exercise_id=exercise_id)
    return Workout.query.filter(*queries).all()


def get_workout_details_json(workout_id):
    workout = get_workout(workout_id)
    response = {}
    response["workout"] = workout_schema.dump(workout)
    response["previous_executions"] = execution_schema.dump(get_previous_executions(workout), many=True)
    response["records"] = get_records(workout)
    return response


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


def set_workout(payload) -> Workout:
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
                reps=s["reps"],
                type=s["type"],
                recovery=s["recovery"]
            ))

    db.session.add(workout)
    db.session.commit()

    return workout


def delete_workout(workout_id):
    db.session.delete(get_workout(workout_id))
    db.session.commit()


def delete_execution(execution_id):
    db.session.delete(get_execution(execution_id))
    db.session.commit()


def get_executions_by_exercise(exercise_id, periodStart=None, periodEnd=None) -> List[Execution]:
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


def get_records(workout: Workout) -> List[dict]:
    records = []

    record_volume_workout = get_best_volume_workout()
    if record_volume_workout == workout:
        value = record_volume_workout.get_volume()
        past_record_workout = get_best_volume_workout(offset=1)
        records.append({
            "code": "WORKOUT_VOLUME",
            "value": value,
            "progress": None if past_record_workout is None else _get_progress_percentage(past_record_workout.get_volume(), value),
            "workout_id": record_volume_workout.id
        })

    for execution in workout.executions:
        record_one_rm_set = get_record_one_rm_set(exercise_id=execution.exercise_id)
        if record_one_rm_set in execution.sets:
            value = record_one_rm_set.get_one_rm()
            past_record_workout = get_record_one_rm_set(exercise_id=execution.exercise_id, offset=1)
            records.append({
                "code": "EXERCISE_SET_ONE_RM",
                "value": round(record_one_rm_set.get_one_rm(), 2),
                "progress": None if past_record_workout is None else _get_progress_percentage(past_record_workout.get_one_rm(), value),
                "execution_id": execution.id,
                "set_id": record_one_rm_set.id
            })

        record_volume_set = get_record_volume_set(exercise_id=execution.exercise_id)
        if record_volume_set in execution.sets:
            value = record_volume_set.get_volume()
            past_record_workout = get_record_volume_set(exercise_id=execution.exercise_id, offset=1)
            records.append({
                "code": "EXERCISE_SET_VOLUME",
                "value": record_volume_set.get_volume(),
                "progress": None if past_record_workout is None else _get_progress_percentage(past_record_workout.get_volume(), value),
                "execution_id": execution.id,
                "set_id": record_volume_set.id
            })

    return records


def get_heatmap():
    workouts = get_workouts()
    heatmap = []

    for w in workouts:
        heatmap.append({
            "date": w.date.timestamp(),
            "value": w.executions.count()
        })

    return heatmap


def _get_progress_percentage(before, after):
    return round(((after - before) / before) * 100, 2)


def _get_queries(exercise_id=None):
    queries = [Workout.user_id == current_user.id]

    if exercise_id is not None:
        exercise_controller.get_exercise(exercise_id)
        queries.append(Workout.executions.any(
            Execution.exercise_id == exercise_id))

    return queries
