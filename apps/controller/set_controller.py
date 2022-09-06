from flask_restful import abort

from apps.model.set import Set
import apps.controller.training_controller as training_controller

def getSet(training_id, set_id):
    set = Set.query.get_or_404(set_id)
    training = training_controller.getTraining(training_id)

    if not training.sets.filter_by(id=set.id).first():
        abort(404) # training doesn't contain this set

    return set
