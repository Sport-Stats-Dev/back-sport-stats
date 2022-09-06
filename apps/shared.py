from flask import g
from werkzeug.local import LocalProxy


db = None
ma = None

current_user = LocalProxy(lambda: g.get('_current_user'))
