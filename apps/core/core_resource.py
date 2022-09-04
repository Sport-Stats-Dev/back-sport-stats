from flask_restful import Resource

from apps.core.decorator import token_required


class AuthResource(Resource):

    method_decorators = [token_required]
