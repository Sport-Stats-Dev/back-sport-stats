from flask import Blueprint

from apps.shared import api
from apps.api.routes import Routes
from apps.api.user_api import LoginApi, UserApi, UserListApi
from apps.api.training_api import TrainingApi, TrainingListApi


load_api_blueprint = Blueprint('load_api_page', __name__, static_folder='static', template_folder='templates')

api.add_resource(UserApi, Routes.USER, Routes.USER_ID)
api.add_resource(UserListApi, Routes.USERS)
api.add_resource(LoginApi, Routes.LOGIN)

api.add_resource(TrainingApi, Routes.TRAINING, Routes.TRAINING_ID)
api.add_resource(TrainingListApi, Routes.TRAININGS)
