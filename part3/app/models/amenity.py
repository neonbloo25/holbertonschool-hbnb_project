#!/usr/bin/python3
import uuid
from datetime import datetime
from app import db
from .base_model import BaseModel

class Amenity(BaseModel):
    """Amenities Table Format"""
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False, unique=True)

    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities')

    def __init__(self, name):
        print(f"🔧 Creating Amenity: {name}")  # Debug
        super().__init__()
        self.name = name.strip()
        print(f"✅ Amenity instance created with name: {self.name}")  # Debug

