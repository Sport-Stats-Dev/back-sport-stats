from flask import Blueprint
from flask_restful import Api

from apps.core.core_resource import CoreResource
from apps.api.routes import Routes
from apps.api.set_api import SetApi, SetListApi
from apps.api.user_api import LoginApi, RegisterApi
from apps.api.training_api import TrainingApi, TrainingListApi
from apps.api.exercise_api import ExerciseApi, ExerciseListApi
from apps.api.average_api import Average1rmPerTrainingsApi, EvolutionOf1rmPerTrainingsApi

class HelloWorldApi(CoreResource):
    def get(self):
        return 'This is SportStats API'

api_blueprint = Blueprint('api', __name__)

api = Api(api_blueprint)

api.add_resource(HelloWorldApi, '/')

api.add_resource(RegisterApi, Routes.REGISTER_PATH)
api.add_resource(LoginApi, Routes.LOGIN_PATH)

api.add_resource(TrainingApi, Routes.TRAINING_ID_PATH)
api.add_resource(TrainingListApi, Routes.TRAINING_PATH)

api.add_resource(SetApi, Routes.SET_ID_PATH)
api.add_resource(SetListApi, Routes.SET_PATH)

api.add_resource(ExerciseApi, Routes.EXERCISE_ID_PATH)
api.add_resource(ExerciseListApi, Routes.EXERCISE_PATH)

api.add_resource(Average1rmPerTrainingsApi, Routes.EXERCISE_AVERAGE_1RM_PATH)
api.add_resource(EvolutionOf1rmPerTrainingsApi, Routes.EXERCISE_EVOL_1RM_PATH)
