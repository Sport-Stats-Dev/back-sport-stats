from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.local import LocalProxy


db = None
ma = None

current_user = LocalProxy(lambda: g.get('_current_user'))


def init_app(app):
    global db, ma
    db = SQLAlchemy(app)
    ma = Marshmallow(app)
