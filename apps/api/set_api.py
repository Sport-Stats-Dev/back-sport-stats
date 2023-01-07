from flask_restful import request

from apps.model.set import set_schema, sets_schema
from apps.core.core_resource import AuthResource
import apps.controller.set_controller as set_controller
import apps.controller.training_controller as training_controller


class SetApi(AuthResource):
    def get(self, training_id, set_id):
        set = set_controller.get_set(training_id, set_id)

        return set_schema.jsonify(set)

    def put(self, training_id, set_id):
        payload = request.get_json()
        set_controller.set_set(payload, training_id, set_id=set_id)

        return 'Success', 200

    def delete(self, training_id, set_id):
        set_controller.delete_set(training_id, set_id)

        return 'Success', 200

class SetListApi(AuthResource):
    def get(self, training_id):
        training = training_controller.get_training(training_id)
        
        return sets_schema.dump(training.sets)

    def post(self, training_id):
        payload = request.get_json()
        set_controller.set_set(payload, training_id)
        
        return 'Success', 200
