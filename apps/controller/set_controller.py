from flask_restful import abort

from apps.model.set import Set
from apps.shared import db
import apps.controller.training_controller as training_controller

def get_set(training_id, set_id) -> Set:
    set = Set.query.get_or_404(set_id)
    training = training_controller.getTraining(training_id)

    if not training.sets.filter_by(id=set.id).first():
        abort(404) # training doesn't contain this set

    return set

def set_set(payload, training_id, set_id=None, commit_database=True):
    order = payload['order']
    reps = payload['reps']
    weight = payload['weight']

    if set_id is not None:
        set = get_set(training_id, set_id)
        set.order = order
        set.reps = reps
        set.weight = weight
    else:
        new_set = Set(training_id, order, reps, weight)
        db.session.add(new_set)

    if commit_database:
        db.session.commit()
