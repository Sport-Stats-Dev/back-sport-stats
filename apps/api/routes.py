class Routes:
    REGISTER_PATH = '/register'
    LOGIN_PATH = '/login'

    CURRENT_USER = '/user'

    TRAINING_PATH = CURRENT_USER + '/trainings'
    TRAINING_ID_PATH = TRAINING_PATH + '/<training_id>'

    SET_PATH = TRAINING_ID_PATH + '/sets'
    SET_ID_PATH = SET_PATH + '/<set_id>'

    EXERCISE_PATH = CURRENT_USER + '/exercises'
    EXERCISE_ID_PATH = EXERCISE_PATH + '/<exercise_id>'
    EXERCISE_ID_DETAILS_PATH = EXERCISE_ID_PATH + '/details'

    ONE_RMS_PATH = EXERCISE_ID_PATH + '/one-rms'
    ONE_RMS_EVOL_PATH = EXERCISE_ID_PATH + '/one-rms-evol'
    VOLUMES_PATH = EXERCISE_ID_PATH + '/volumes'
    VOLUMES_EVOL_PATH = EXERCISE_ID_PATH + '/volumes-evol'
