from datetime import datetime, timedelta
import uuid

from apps.shared import db, ma
from apps.model.training import TrainingSchema


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    create_date = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow
    )

    last_connexion = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    expiration_date = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow()+timedelta(days=31)
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

    trainings = db.relationship(
        "Training",
        order_by="Training.id"
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
    
    trainings = ma.Nested(TrainingSchema, many=True) 

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

full_user_schema = FullUserSchema()
full_users_schema = FullUserSchema(many=True)
