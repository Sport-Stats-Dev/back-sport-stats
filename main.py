import datetime
from flask import Flask, g
from apps.core.tools import add_token_to_response, refresh_access_token
from apps import shared
from dotenv import load_dotenv
import os


# Init app
app = Flask(__name__)

# Config
load_dotenv()
app.config["SQLALCHEMY_DATABASE_URI"] = \
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db_postgres/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))

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

# Run Server (if not using flask run)
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)
