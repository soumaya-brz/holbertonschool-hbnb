from app.models.base_model import BaseModel, ValidationError
from app import db


class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Relations ajoutées plus tard
    place_id = db.Column(db.String(36), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)

    def __init__(self, text, rating, place=None, user=None, place_id=None, user_id=None):
        super().__init__()

        self.text = text
        self.rating = int(rating)

        if place:
            self.place_id = place.id
        else:
            self.place_id = place_id

        if user:
            self.user_id = user.id
        else:
            self.user_id = user_id

        self.validate()

    def validate(self):
        if not self.text or not isinstance(self.text, str):
            raise ValidationError("text is required")

        if not (1 <= self.rating <= 5):
            raise ValidationError("rating must be between 1 and 5")

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id
        })
        return base