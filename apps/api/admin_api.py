from flask import abort
from apps.shared import current_user
from apps.core.core_resource import AuthResource
from apps.utils import shared_exercise_utils


class UpdateSharedExercises(AuthResource):
    def get(self):
        # TODO: FAIRE UN VRAI SYSTEME DE PERMISSIONS
        if (current_user.email != "aa@gmail.com"):
            abort(403)
        shared_exercise_utils.fill_database()
        return "Success", 200
