#!/usr/bin/python3
import uuid
from app import db, bcrypt
from .base_model import BaseModel
from datetime import datetime
import re
from .place import Place

class User(BaseModel):
    """User Table Formatting"""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', back_populates='owner', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        print(f"🔧 Creating User: {first_name} {last_name} | Email: {email}")  # Debug
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List to store places owned by the user

        if password:
            self.hash_password(password)
            print("🔐 Password hashed and set.")  # Debug
        print("✅ User instance created.")  # Debug

    def hash_password(self, password):
        """Hashes the password before storing it."""
        print("🔐 Hashing password...")  # Debug
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        print("✅ Password hashed.")  # Debug

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        print("🔍 Verifying password...")  # Debug
        result = bcrypt.check_password_hash(self.password_hash, password)
        print(f"✅ Password verification result: {result}")  # Debug
        return result

    def add_place(self, place):
        """Add a place to the user's list of owned places."""
        print(f"📦 Adding place to user {self.email}")  # Debug
        if not isinstance(place, Place):
            print("❌ Invalid place object provided.")  # Debug
            raise ValueError("The provided place must be an instance of Place.")
        self.places.append(place)
        print("✅ Place added to user's places.")  # Debug
