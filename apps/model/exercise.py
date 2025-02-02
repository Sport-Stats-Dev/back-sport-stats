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
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(2000)
    )

    primary_muscle = db.Column(
        db.String(100),
        nullable=False
    )

    secondary_muscles = db.Column(
        db.String(100)
    )

    equipments = db.Column(
        db.String(100)
    )

    __mapper_args__ = {
        'polymorphic_identity': 'exercise',
        'polymorphic_on': 'type',
    }

    def __init__(
            self,
            name,
            primary_muscle,
            description=None,
            secondary_muscles=None,
            equipments=None
            ):
        self.name = name
        self.description = description
        self.primary_muscle = primary_muscle
        self.secondary_muscles = secondary_muscles
        self.equipments = equipments


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

    def __init__(
            self,
            name,
            primary_muscle,
            image,
            video,
            description=None,
            secondary_muscles=None,
            equipments=None
            ):
        super().__init__(name, primary_muscle, description, secondary_muscles, equipments)
        self.image = image
        self.video = video
        self.name = name
        self.description = description
        self.primary_muscle = primary_muscle
        self.secondary_muscles = secondary_muscles
        self.equipments = equipments


class UserExercise(Exercise):
    __tablename__ = 'user_exercise'

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id")
    )

    __mapper_args__ = {
        'polymorphic_identity': 'user',
    }

    def __init__(
            self,
            user_id,
            name,
            primary_muscle,
            description=None,
            secondary_muscles=None,
            equipments=None
            ):
        super().__init__(name, primary_muscle, description, secondary_muscles, equipments)
        self.user_id = user_id
        self.name = name
        self.description = description
        self.primary_muscle = primary_muscle
        self.secondary_muscles = secondary_muscles
        self.equipments = equipments


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
