

from flask_restful import abort
from apps.controller import workout_controller
from apps.core.core_resource import AuthResource
from apps.model.execution import execution_schema


class ExecutionApi(AuthResource):
    def get(self, execution_id):
        execution = workout_controller.get_execution(execution_id=execution_id)

        if execution is None:
            abort(404) # not found
        
        response = execution_schema.dump(execution)
        response["date"] = str(execution.workout.date)

        return response