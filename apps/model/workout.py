import uuid
from apps.model.execution import ExecutionSchema
from apps.shared import db, ma


class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id"),
        nullable=False
    )

    name = db.Column(
        db.String(200)
    )

    date = db.Column(
        db.DateTime,
        nullable=False
    )

    duration = db.Column(
        db.Integer,
        nullable=False
    )

    notes = db.Column(
        db.String(2000)
    )

    executions = db.relationship(
        "Execution",
        order_by="Execution.order",
        backref="workout",
        lazy="dynamic",
        cascade='all, delete-orphan'
    )

    def __init__(self, user_id, name, date, duration, notes):
        self.user_id = user_id
        self.name = name
        self.date = date
        self.duration = duration
        self.notes = notes

class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        ordered = True
    
    executions = ma.Nested(ExecutionSchema, many=True)

# Init schema
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
