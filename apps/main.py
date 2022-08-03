from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db & ma
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Load APIs
from api.user_api import user_blueprint
app.register_blueprint(user_blueprint)

# Create database
from model.user import *
db.create_all()

# Hello World
@app.route('/', methods=['GET'])
def hello_sportstats():
  return 'This is SportStats API'

# Run Server
if __name__ == '__main__':
  app.run(debug=True)
