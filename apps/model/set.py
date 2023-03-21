import uuid
from apps.shared import db, ma


class Set(db.Model):
    __tablename__ = 'set'

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    
    execution_id = db.Column(
        db.String(36),
        db.ForeignKey("execution.id"),
        nullable=False
    )

    order = db.Column(
        db.Integer,
        nullable=False
    )

    weight = db.Column(
        db.Float,
        nullable=False
    )

    reps = db.Column(
        db.Integer,
        nullable=False
    )

    def __init__(self, order, weight, reps):
        self.order = order
        self.weight = weight
        self.reps = reps

    def get_one_rm(self):
        return (self.weight * self.reps / 30) + self.weight

class SetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Set
        ordered = True

# Init schema
set_schema = SetSchema()
sets_schema = SetSchema(many=True)
