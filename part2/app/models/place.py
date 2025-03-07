import uuid
from datetime import datetime

from app.models.amenity import Amenity
from app.models.review import Review

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        # Automatically add the place to the owner's places
        owner.add_place(self)

    def add_review(self, review):
        """Add a review to the place."""
        if not isinstance(review, Review):
            raise ValueError("The review must be an instance of Review.")
        if review.place != self:
            raise ValueError("The review's place must match this place.")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if not isinstance(amenity, Amenity):
            raise ValueError("The amenity must be an instance of Amenity.")
        self.amenities.append(amenity)
