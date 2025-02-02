from typing import List, Tuple
from flask_restful import abort
from apps.model.execution import Execution

from apps.model.exercise import Exercise, SharedExercise, UserExercise
from apps.shared import db, current_user
import apps.controller.workout_controller as workout_controller


def get_exercise(exercise_id) -> Exercise:
    exercise = Exercise.query.get_or_404(exercise_id)

    if isinstance(exercise, UserExercise) and exercise.user_id != current_user.id:
        abort(403)  # not user's exercise

    return exercise


def get_paginated_exercises(page=None, per_page=None, order=None, name=None) -> Tuple[List[Exercise], int]:
    queries = [UserExercise.__table__.c.id == Exercise.id and UserExercise.user_id == current_user.id]

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


def get_all_exercises() -> List[Exercise]:
    user_exercises = UserExercise.query.filter_by(user_id=current_user.id).all()
    shared_exercises = SharedExercise.query.all()

    return user_exercises + shared_exercises


def set_exercise(payload, exercise_id=None) -> UserExercise:
    name = payload.get("name")
    description = payload.get("description")
    primary_muscle = payload.get("primary_muscle")
    secondary_muscles = payload.get("secondary_muscles")
    equipments = payload.get("equipments")

    if exercise_id is not None:
        exercise = get_exercise(exercise_id)

        if isinstance(exercise, SharedExercise):
            abort(403)

        exercise.name = name
        exercise.description = description
        exercise.primary_muscle = primary_muscle
        exercise.secondary_muscles = secondary_muscles
        exercise.equipments = equipments
    else:
        exercise = UserExercise(
            user_id=current_user.id,
            name=name,
            description=description,
            primary_muscle=primary_muscle,
            secondary_muscles=secondary_muscles,
            equipments=equipments
        )
        db.session.add(exercise)

    db.session.commit()

    return exercise


def delete_exercise(exercise_id):
    exercise = get_exercise(exercise_id)

    if isinstance(exercise, SharedExercise):
        abort(403)

    for executions in workout_controller.get_executions_by_exercise(exercise_id=exercise_id):
        workout = executions.workout
        workout_controller.delete_execution(executions.id)
        if workout.executions.count() == 0:
            workout_controller.delete_workout(workout.id)

    db.session.delete(exercise)
    db.session.commit()


def merge_exercises(payload):
    exercise_id = payload.get("exercise_id")
    target_id = payload.get("target_id")

    if exercise_id is None or target_id is None or exercise_id == target_id:
        abort(400)

    exercise = get_exercise(exercise_id)
    get_exercise(target_id)

    for execution in workout_controller.get_executions_by_exercise(exercise_id=exercise_id):
        execution.exercise_id = target_id

    if isinstance(exercise, UserExercise):
        db.session.delete(exercise)

    db.session.commit()
