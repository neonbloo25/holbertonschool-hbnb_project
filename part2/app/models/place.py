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
        super().__init__()
        self.title = self._validate_string(title, "Title")
        self.description = self._validate_string(description, "Description")
        self.price = self._validate_price(price)
        self.latitude = self._validate_coordinate(latitude, "Latitude")
        self.longitude = self._validate_coordinate(longitude, "Longitude")
        self.owner = self._validate_owner(owner)
        self.reviews = []  # list to store related reviews
        self.amenities = []  # list to store related amenities

    def _validate_string(self, value, field_name):
        """Validates that a value is a non-empty string"""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return value.strip()

    def _validate_price(self, value):
        """Validates that price is a positive float."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a positive number")
        return float(value)

    def _validate_coordinate(self, value, field_name):
        """Validates latitude/longitude as a valid float."""
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError(f"{field_name} must be a valid coordinate")
        return float(value)

    def _validate_owner(self, owner):
        """Validates that the owner is a valid User"""
        if not isinstance(owner, User):
            raise ValueError("Owner must be a User")
        return owner.id

    def add_review(self, review):
        """Add a review to the place."""
        from .review import Review

        if not isinstance(review, Review):
            raise ValueError("Invalid review")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        from .amenity import Amenity

        if not isinstance(amenity, Amenity):
            raise ValueError("Invalid amenity")
        self.amenities.append(amenity)

    def __repr__(self):
        return (f"Place(title='{self.title}', price={self.price}, "
                f"latitude={self.latitude}, longitude={self.longitude}, "
                f"owner='{self.owner}', reviews={len(self.reviews)}, "
                f"amenities={len(self.amenities)})")
