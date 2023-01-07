from apps.shared import db, ma


class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(2000)
    )

    training_count = db.Column(
        db.Integer,
        default=0
    )

    def __init__(self, user_id, name, description):
        self.user_id = user_id
        self.name = name
        self.description = description

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        ordered = True

# Init schema
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
