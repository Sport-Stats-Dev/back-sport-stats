class Routes:
    REGISTER_PATH = '/register'
    LOGIN_PATH = '/login'

    CURRENT_USER = '/user'

    TRAINING_PATH = CURRENT_USER + '/trainings'
    TRAINING_ID_PATH = TRAINING_PATH + '/<training_id>'

    SET_PATH = TRAINING_ID_PATH + '/sets'
    SET_ID_PATH = SET_PATH + '/<set_id>'
