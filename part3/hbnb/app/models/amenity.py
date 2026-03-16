from app.models.base_model import BaseModel, ValidationError
from app import db


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
        if not self.name or not isinstance(self.name, str):
            raise ValidationError("name is required")

        if len(self.name) > 50:
            raise ValidationError("name must be <= 50 characters")

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "name": self.name
        })
        return base