from flask_restful import abort
import datetime

from apps.model.training import Training
from apps.shared import current_user

def getTraining(training_id):
    training = Training.query.get_or_404(training_id)

    if training.user_id != current_user.id:
        abort(403) # not user's training

    return training

def formatDate(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
