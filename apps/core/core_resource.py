from flask_restful import Resource

from apps.core.decorator import authenticate, auth_requiered


class CoreResource(Resource):

    method_decorators = [authenticate]

class AuthResource(Resource):

    method_decorators = [authenticate, auth_requiered]
