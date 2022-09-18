from flask import Blueprint
from flask_restful import Api

from apps.api.routes import Routes
from apps.api.set_api import SetApi, SetListApi
from apps.api.user_api import LoginApi, RegisterApi
from apps.api.training_api import TrainingApi, TrainingListApi
from apps.core.core_resource import CoreResource

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