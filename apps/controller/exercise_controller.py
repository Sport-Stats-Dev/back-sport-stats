from flask_restful import abort

from apps.model.exercise import Exercise
from apps.shared import db, current_user
import apps.controller.training_controller as training_controller

def get_exercise(exercise_id) -> Exercise:
    exercise = Exercise.query.get_or_404(exercise_id)

    if exercise.user_id != current_user.id:
        abort(403) # not user's exercise

    return exercise

def set_exercise(payload, exercise_id=None):
    name = payload['name']
    description = payload['description']

    if exercise_id is not None:
        exercise = get_exercise(exercise_id)
        exercise.name = name
        exercise.description = description
    else:
        new_set = Exercise(current_user.id, name, description)
        db.session.add(new_set)
    
    db.session.commit()

def delete_exercise(exercise_id):
    exercise = get_exercise(exercise_id)

    for training in training_controller.get_trainings(exercise_id=exercise_id):
        training_controller.delete_training(training.id, commit_database=False)

    db.session.delete(exercise)
    db.session.commit()
