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

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self.set_name(name)

    def set_name(self, name):
        """Ensures the name is required and within the 50-character limit."""
        if not name or len(name) == 0:
            raise ValueError("Amenity name is required.")
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters.")
        return name
