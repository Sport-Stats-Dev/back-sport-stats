from main import db, ma


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), nullable=False, unique=True)
  username = db.Column(db.String(50), nullable=False, unique=True)
  password = db.Column(db.String(255), nullable=False)

  def __init__(self, email, username, password):
    self.email = email
    self.username = username
    self.password = password

class UserSchema(ma.Schema):
  class Meta:
    fields = (
      'id',
      'email',
      'username',
      'password'
    )

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
