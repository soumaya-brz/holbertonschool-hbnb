from app.models.base_model import BaseModel
from app import db


place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    reviews = db.relationship("Review", backref="place", lazy=True, cascade="all, delete-orphan")

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        backref=db.backref("places", lazy=True),
        lazy=True
    )

    def __init__(self, title, description, price, latitude, longitude, owner=None, owner_id=None):
        super().__init__()

        self.title = title
        self.description = description or ""
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)

        if owner:
            self.owner_id = owner.id
        else:
            self.owner_id = owner_id

        self.validate()

    def validate(self):
        if not self.title or not isinstance(self.title, str):
            raise ValueError("title is required")

        if len(self.title) > 100:
            raise ValueError("title must be <= 100 characters")

        if self.price <= 0:
            raise ValueError("price must be positive")

        if not (-90 <= self.latitude <= 90):
            raise ValueError("latitude must be between -90 and 90")

        if not (-180 <= self.longitude <= 180):
            raise ValueError("longitude must be between -180 and 180")

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [a.id for a in self.amenities],
            "reviews": [r.id for r in self.reviews]
        })
        return base