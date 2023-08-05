from flask import Blueprint
from flask_restful import Api
from apps.api.execution_api import ExecutionApi

from apps.core.core_resource import CoreResource
from apps.api.routes import Routes
from apps.api.user_api import LoginApi, RegisterApi
from apps.api.workout_api import WorkoutApi, WorkoutListApi
from apps.api.exercise_api import ExerciseApi, ExerciseDetailsApi, ExerciseLastExecutionApi, ExerciseListApi
from apps.api.stats_api import OneRmsApi, OneRmsEvolApi, VolumesApi, VolumesEvolApi, MaxWeightApi

class HelloWorldApi(CoreResource):
    def get(self):
        return 'This is SportStats API'

api_blueprint = Blueprint('api', __name__)

api = Api(api_blueprint)

api.add_resource(HelloWorldApi, '/')

api.add_resource(RegisterApi, Routes.REGISTER_PATH)
api.add_resource(LoginApi, Routes.LOGIN_PATH)

api.add_resource(WorkoutApi, Routes.WORKOUT_ID_PATH)
api.add_resource(WorkoutListApi, Routes.WORKOUT_PATH)

api.add_resource(ExecutionApi, Routes.EXECUTION_ID_PATH)

api.add_resource(ExerciseApi, Routes.EXERCISE_ID_PATH)
api.add_resource(ExerciseListApi, Routes.EXERCISE_PATH)
api.add_resource(ExerciseDetailsApi, Routes.EXERCISE_ID_DETAILS_PATH)
api.add_resource(ExerciseLastExecutionApi, Routes.EXERCISE_ID_LAST_EXECUTION_PATH)

api.add_resource(OneRmsApi, Routes.ONE_RMS_PATH)
api.add_resource(OneRmsEvolApi, Routes.ONE_RMS_EVOL_PATH)
api.add_resource(VolumesApi, Routes.VOLUMES_PATH)
api.add_resource(VolumesEvolApi, Routes.VOLUMES_EVOL_PATH)
api.add_resource(MaxWeightApi, Routes.MAX_WEIGHT_PATH)
