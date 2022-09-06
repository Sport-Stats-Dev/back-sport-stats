from flask_restful import request

from apps.model.set import Set, set_schema, sets_schema
from apps.shared import db
from apps.core.core_resource import AuthResource
import apps.controller.set_controller as controller
import apps.controller.training_controller as training_controller


class SetApi(AuthResource):
    def get(self, training_id, set_id):
        set = controller.getSet(training_id, set_id)

        return set_schema.jsonify(set)

    def put(self, training_id, set_id):
        set = controller.getSet(training_id, set_id)
        payload = request.get_json()

        order = payload['order']
        reps = payload['reps']
        weight = payload['weight']

        set.order = order
        set.reps = reps
        set.weight = weight

        db.session.commit()

        return 'Success', 200

    def delete(self, training_id, set_id):
        set = controller.getSet(training_id, set_id)

        db.session.delete(set)
        db.session.commit()

        return 'Success', 200

class SetListApi(AuthResource):
    def get(self, training_id):
        training = training_controller.getTraining(training_id)
        
        return sets_schema.dump(training.sets)

    def post(self, training_id):
        payload = request.get_json()

        order = payload['order']
        reps = payload['reps']
        weight = payload['weight']

        new_set = Set(training_id, order, reps, weight)
        db.session.add(new_set)
        db.session.commit()
        
        return 'Success', 200
