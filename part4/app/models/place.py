import uuid
from datetime import datetime
from app import db
from .base_model import BaseModel

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Place Table Format"""
    __tablename__ = "places"

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place', cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places')

    def __init__(self, title, price, latitude, longitude, owner, description=None):
        print("🔧 Creating Place instance...")  # Debug
        super().__init__()
        self.title = self._validate_string(title, "Title")
        self.description = self._validate_string(description, "Description")
        self.price = self._validate_price(price)
        self.latitude = self._validate_coordinate(latitude, "Latitude")
        self.longitude = self._validate_coordinate(longitude, "Longitude")
        self.owner = self._validate_owner(owner)
        self.reviews = []
        self.amenities = []
        print(f"✅ Place created: {self.title} (${self.price}) at ({self.latitude}, {self.longitude})")  # Debug

    def _validate_string(self, value, field_name):
        print(f"🔍 Validating string field: {field_name}")  # Debug
        if not isinstance(value, str) or not value.strip():
            print(f"❌ {field_name} validation failed.")  # Debug
            raise ValueError(f"{field_name} must be a non-empty string")
        print(f"✅ {field_name} is valid.")  # Debug
        return value.strip()

    def _validate_price(self, value):
        print("🔍 Validating price...")  # Debug
        if not isinstance(value, (int, float)) or value < 0:
            print("❌ Invalid price.")  # Debug
            raise ValueError("Price must be a positive number")
        print
