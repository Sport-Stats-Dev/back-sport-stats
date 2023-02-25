import uuid
from apps.model.exercise import ExerciseSchema
from apps.model.set import SetSchema
from apps.shared import db, ma


class Training(db.Model):
    __tablename__ = 'training'

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    
    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercise.id"),
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False
    )

    comment = db.Column(
        db.String(2000)
    )

    sets = db.relationship(
        "Set",
        order_by="Set.order",
        lazy="dynamic"
    )

    exercise = db.relationship(
        "Exercise",
        order_by="Exercise.id"
    )

    def __init__(self, user_id, exercise_id, date, comment):
        self.user_id = user_id
        self.exercise_id = exercise_id
        self.date = date
        self.comment = comment

    def get_one_rm_average(self):
        return sum([s.get_one_rm() for s in self.sets]) / self.sets.count()
    
    def get_volume(self):
        return sum([s.weight * s.reps for s in self.sets])

class TrainingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Training
        ordered = True
    
    sets = ma.Nested(SetSchema, many=True)
    exercise = ma.Nested(ExerciseSchema)

# Init schema
training_schema = TrainingSchema()
trainings_schema = TrainingSchema(many=True)
