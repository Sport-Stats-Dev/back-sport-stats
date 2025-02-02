import uuid
from apps.shared import db, ma


class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    type = db.Column(
        db.String(50),
        nullable=False
    )

    name = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.String(2000)
    )

    __mapper_args__ = {
        'polymorphic_identity': 'exercise',
        'polymorphic_on': 'type',
    }

    def __init__(self, name, description):
        self.name = name
        self.description = description

class SharedExercise(Exercise):
    __tablename__ = 'shared_exercise'

    image = db.Column(
        db.String(200)
    )

    video = db.Column(
        db.String(200)
    )

    __mapper_args__ = {
        'polymorphic_identity': 'shared',
    }

    def __init__ (self, name, description, image=None, video=None):
        super().__init__(name, description)
        self.image = image
        self.video = video

class UserExercise(Exercise):
    __tablename__ = 'user_exercise'
    
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id")
    )

    __mapper_args__ = {
        'polymorphic_identity': 'user',
    }

    def __init__ (self, name, description, user_id):
        super().__init__(name, description)
        self.user_id = user_id
        self.name = name
        self.description = description

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        ordered = True

    image = ma.Method("get_image")
    def get_image(self, obj):
        if obj.type == "shared":
            return obj.image
        else:
            return None
    video = ma.Method("get_video")
    def get_video(self, obj):
        if obj.type == "shared":
            return obj.video
        else:
            return None

# Init schema
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
