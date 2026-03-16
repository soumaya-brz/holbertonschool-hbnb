import re
from flask_bcrypt import generate_password_hash, check_password_hash
from app.models.base_model import BaseModel
from app import db

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship("Place", backref="owner", lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship("Review", backref="user", lazy=True, cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)
        self.password_hash = generate_password_hash(password).decode("utf-8")
        self.validate()

    def validate(self):
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("first_name is required and must be <= 50 characters")

        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("last_name is required and must be <= 50 characters")

        if not self.email or not EMAIL_RE.match(self.email):
            raise ValueError("email is required and must be valid")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return base