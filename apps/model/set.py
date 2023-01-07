import uuid
from apps.shared import db, ma


class Set(db.Model):
    __tablename__ = 'set'

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    
    training_id = db.Column(
        db.Integer,
        db.ForeignKey("training.id"),
        nullable=False
    )

    order = db.Column(
        db.Integer,
        nullable=False
    )

    reps = db.Column(
        db.Integer,
        nullable=False
    )

    weight = db.Column(
        db.Float,
        nullable=False
    )

    def __init__(self, training_id, order, reps, weight):
        self.training_id = training_id
        self.order = order
        self.reps = reps
        self.weight = weight

class SetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Set
        ordered = True

# Init schema
set_schema = SetSchema()
sets_schema = SetSchema(many=True)
