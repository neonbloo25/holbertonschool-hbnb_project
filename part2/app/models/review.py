import uuid
from datetime import datetime

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

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.set_text(text)
        self.rating = self.set_rating(rating)
        self.place = place
        self.user = user

    def set_text(self, text):
        """Ensures the text is provided (required field)."""
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text is required and cannot be empty.")
        return text

    def set_rating(self, rating):
        """Ensures the rating is between 1 and 5."""
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        return rating
