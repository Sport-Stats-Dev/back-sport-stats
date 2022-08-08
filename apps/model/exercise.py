from apps.shared import db, ma


class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    feeling = db.Column(db.Integer)
    comment = db.Column(db.String(2000))

    def __init__(self, user_id, date, feeling, comment):
        self.user_id = user_id
        self.date = date
        self.feeling = feeling
        self.comment = comment

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        ordered = True

# Init schema
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
