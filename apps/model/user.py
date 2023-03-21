from datetime import datetime, timedelta
import uuid

from apps.shared import db, ma
import apps.model.workout


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

    workouts = db.relationship(
        "Workout",
        backref="user",
        lazy="dynamic",
        cascade='all, delete-orphan'
    )

    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        ordered = True

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
