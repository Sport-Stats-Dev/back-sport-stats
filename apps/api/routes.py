class Routes:
    REGISTER_PATH = '/register'
    LOGIN_PATH = '/login'
    REFRESH_PATH = '/refresh'

    CURRENT_USER = '/user'

    WORKOUT_PATH = CURRENT_USER + '/workouts'
    WORKOUT_ID_PATH = WORKOUT_PATH + '/<workout_id>'
    WORKOUT_HEATMAP_PATH = WORKOUT_PATH + '/heatmap'
    WORKOUT_ID_DETAILS_PATH = WORKOUT_ID_PATH + '/details'

    EXECUTION_ID_PATH = CURRENT_USER + '/executions/<execution_id>'

    EXERCISE_PATH = CURRENT_USER + '/exercises'
    EXERCISE_ID_PATH = EXERCISE_PATH + '/<exercise_id>'
    EXERCISE_ID_DETAILS_PATH = EXERCISE_ID_PATH + '/details'
    EXERCISE_ID_LAST_EXECUTION_PATH = EXERCISE_ID_PATH + '/last-execution'

    EXERCISES_MERGE_PATH = EXERCISE_PATH + '/merge'

    ONE_RMS_PATH = EXERCISE_ID_PATH + '/one-rms'
    ONE_RMS_EVOL_PATH = EXERCISE_ID_PATH + '/one-rms-evol'
    VOLUMES_PATH = EXERCISE_ID_PATH + '/volumes'
    VOLUMES_EVOL_PATH = EXERCISE_ID_PATH + '/volumes-evol'
    MAX_WEIGHT_PATH = EXERCISE_ID_PATH + '/max-weight'

    UPDATE_SHARED_EXERICISES = '/admin/update-shared-exercises'
