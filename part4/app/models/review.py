import uuid
from app import db
from datetime import datetime
from .base_model import BaseModel
from .place import Place
from .user import User

class Review(BaseModel):
    """Review Table Format"""
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
    )

    def __init__(self, text, rating, place, user):
        print("🔧 Creating Review instance...")  # Debug
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place = self._validate_place(place)
        self.user_id = self._validate_user(user)
        print(f"✅ Review created for place ID {self.place} by user ID {self.user_id}")  # Debug

    def _validate_text(self, text):
        print("🔍 Validating review text...")  # Debug
        if not isinstance(text, str) or not text.strip():
            print("❌ Invalid review text.")  # Debug
            raise ValueError("Review text must be a non-empty string")
        print("✅ Review text valid.")  # Debug
        return text.strip()

    def _validate_rating(self, rating):
        print(f"🔍 Validating rating: {rating}")  # Debug
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            print("❌ Rating out of range.")  # Debug
            raise ValueError("Rating must be an integer between 1 and 5")
        print("✅ Rating is valid.")  # Debug
        return rating

    def _validate_place(self, place):
        print("🔍 Validating place...")  # Debug
        if not isinstance(place, Place):
            print("❌ Invalid place instance.")  # Debug
            raise ValueError("Place must be a valid Place instance")
        print(f"✅ Place valid with ID: {place.id}")  # Debug
        return place.id

    def _validate_user(self, user):
        print("🔍 Validating user...")  # Debug
        if not isinstance(user, User):
            print("❌ Invalid user instance.")  # Debug
            raise ValueError("User must be a valid User instance")
        print(f"✅ User valid with ID: {user.id}")  # Debug
        return user.id
