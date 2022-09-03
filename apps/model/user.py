from apps.shared import db, ma
from apps.model.exercise import ExerciseSchema


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )
    
    password = db.Column(
        db.String(255),
        nullable=False
    )

    exercises = db.relationship(
        "Exercise",
        order_by="Exercise.id"
    )

    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        ordered = True

class FullUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        ordered = True
    
    exercises = ma.Nested(ExerciseSchema, many=True) 

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

full_user_schema = FullUserSchema()
full_users_schema = FullUserSchema(many=True)
