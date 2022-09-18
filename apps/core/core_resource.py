from flask_restful import Resource

from apps.core.decorator import auth, auth_requiered


class CoreResource(Resource):

    method_decorators = [auth]

class AuthResource(Resource):

    method_decorators = [auth_requiered]
