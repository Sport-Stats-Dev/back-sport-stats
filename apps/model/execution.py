import uuid
from apps.model.exercise import ExerciseSchema
from apps.model.set import SetSchema
from apps.shared import db, ma


class Execution(db.Model):
    __tablename__ = 'execution'

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    
    workout_id = db.Column(
        db.String(36),
        db.ForeignKey("workout.id"),
        nullable=False
    )
    
    exercise_id = db.Column(
        db.String(36),
        db.ForeignKey("exercise.id"),
        nullable=False
    )

    order = db.Column(
        db.Integer,
        nullable=False
    )

    notes = db.Column(
        db.String(2000)
    )

    sets = db.relationship(
        "Set",
        order_by="Set.order",
        lazy="dynamic",
        cascade='all, delete-orphan'
    )

    exercise = db.relationship(
        "Exercise",
        order_by="Exercise.id"
    )

    def __init__(self, exercise_id, order, notes):
        self.exercise_id = exercise_id
        self.order = order
        self.notes = notes

    def get_one_rm_average(self):
        return sum([s.get_one_rm() for s in self.sets if s.type == 0]) / len([s for s in self.sets if s.type == 0])
    
    def get_volume(self):
        return sum([s.weight * s.reps for s in self.sets])
    
    def get_max_weight(self):
        return max([s.weight for s in self.sets])

class ExecutionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Execution
        ordered = True
    
    sets = ma.Nested(SetSchema, many=True)
    exercise_id = ma.auto_field()

# Init schema
execution_schema = ExecutionSchema()
executions_schema = ExecutionSchema(many=True)
