from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
import os
import apps.shared as shared


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'thisissecret'

# Inits
shared.db = SQLAlchemy(app)
shared.ma = Marshmallow(app)
shared.api = Api(app)

# Load APIs
from apps.api.load_api import load_api_blueprint
app.register_blueprint(load_api_blueprint)

# Hello World
@app.route('/', methods=['GET'])
def hello_sportstats():
    return 'This is SportStats API'


from apps.model.user import *
from apps.model.exercise import *
shared.db.create_all()

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
