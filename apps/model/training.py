from apps.model.set import SetSchema
from apps.shared import db, ma


class Training(db.Model):
    __tablename__ = 'training'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
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
        order_by="Set.id",
        lazy="dynamic"
    )

    def __init__(self, user_id, date, comment):
        self.user_id = user_id
        self.date = date
        self.comment = comment

class TrainingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Training
        ordered = True
    
    sets = ma.Nested(SetSchema, many=True) 

# Init schema
training_schema = TrainingSchema()
trainings_schema = TrainingSchema(many=True)
