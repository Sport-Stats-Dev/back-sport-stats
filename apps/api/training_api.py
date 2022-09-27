from flask_restful import request

from apps.model.training import Training, training_schema, trainings_schema
from apps.shared import db, current_user
from apps.core.core_resource import AuthResource
import apps.controller.training_controller as training_controller
import apps.controller.set_controller as set_controller
import apps.controller.exercise_controller as exercise_controller


class TrainingApi(AuthResource):
    def get(self, training_id):
        training = training_controller.get_training(training_id)

        return training_schema.jsonify(training)
        
    def put(self, training_id):
        training = training_controller.get_training(training_id)
        payload = request.get_json()

        exercise_id = exercise_controller.get_exercise(payload['exercise_id']).id
        date = training_controller.format_date(payload['date'])
        comment = payload['comment']

        training.exercise_id = exercise_id
        training.date = date
        training.comment = comment

        db.session.commit()

        return 'Success', 200

    def delete(self, training_id):
        training = training_controller.get_training(training_id)

        db.session.delete(training)
        db.session.commit()
        
        return 'Success', 200

class TrainingListApi(AuthResource):
    def get(self):
        trainings = Training.query.filter_by(user_id=current_user.id).all()

        print(trainings)
        print(trainings[0].exercise_id)
        
        return trainings_schema.dump(trainings)
    
    def post(self):
        payload = request.get_json()

        exercise_id = exercise_controller.get_exercise(payload['exercise_id']).id
        date = training_controller.format_date(payload['date'])
        comment = payload['comment']

        new_training = Training(current_user.id, exercise_id, date, comment)
        db.session.add(new_training)
        db.session.commit()
        
        if payload['sets']:
            sets = payload['sets']
            for set in sets:
                set_controller.set_set(set, new_training.id, commit_database=False)
        
        db.session.commit()

        return 'Success', 200
