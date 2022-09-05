class Routes:
    USER = '/user'
    USER_ID = USER + '/<id>'
    USERS = USER + 's'

    LOGIN = '/login'

    CURRENT_USER = '/user'

    TRAINING = CURRENT_USER + '/training'
    TRAINING_ID = TRAINING + '/<id>'
    TRAININGS = TRAINING + 's'
