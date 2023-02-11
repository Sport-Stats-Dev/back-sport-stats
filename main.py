import datetime
from flask import Flask, g
import os
from apps.core.tools import add_token_to_response, refresh_access_token
from apps import shared


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
app.config['TOKEN_VALIDITY'] = datetime.timedelta(minutes=30)

# Inits
shared.init_app(app)

from apps import model
shared.db.create_all()

# Load blueprints
from apps.api import api_blueprint
app.register_blueprint(api_blueprint)

@app.after_request
def generate_new_token(response):
    access_token = getattr(g, 'access_token', None)

    if access_token is not None:
        new_token = refresh_access_token(access_token)
        add_token_to_response(response, new_token)

    return response

@app.after_request
def cors(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
    response.headers.add("Access-Control-Allow-Headers", "content-type")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Allow-Methods", "PUT, POST, GET, DELETE")
    return response

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
