from flask import g
from flask_restful import request, abort
import datetime

from apps.model.training import Training, training_schema, trainings_schema
from apps.shared import db
from apps.core.core_resource import AuthResource


class TrainingApi(AuthResource):
    def post(self):
        current_user = getattr(g, '_current_user', None)
        payload = request.get_json()

        date = _formatDate(payload['date'])
        comment = payload['comment']

        new_training = Training(current_user.id, date, comment)
        db.session.add(new_training)
        db.session.commit()
        
        return 'Success', 200
        
    def get(self, id):
        training = _getTraining(id)

        return training_schema.jsonify(training)
        
    def put(self, id):
        training = _getTraining(id)
        payload = request.get_json()

        training.date = _formatDate(payload['date'])
        training.comment = payload['comment']

        db.session.commit()

        return 'Success', 200

    def delete(self, id):
        training = _getTraining(id)

        db.session.delete(training)
        db.session.commit()
        
        return 'Success', 200

def _getTraining(id):
    current_user = getattr(g, '_current_user', None)
    training = Training.query.get_or_404(id)

    if training.user_id != current_user.id:
        return abort(401) # not user's training

    return training

def _formatDate(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        

class TrainingListApi(AuthResource):
    def get(self):
        current_user = getattr(g, '_current_user', None)

        trainings = Training.query.filter_by(user_id=current_user.id).all()
        
        return trainings_schema.dump(trainings)
