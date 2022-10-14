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

    EXERCISE_AVERAGE_1RM_PATH = EXERCISE_ID_PATH + '/1rm-average-per-trainings'
    EXERCISE_EVOL_1RM_PATH = EXERCISE_ID_PATH + '/evolution-of-1rm-per-trainings'
