from main import db, ma


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(100))

  def __init__(self, username, password):
    self.username = username
    self.password = password

class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username', 'password')

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
