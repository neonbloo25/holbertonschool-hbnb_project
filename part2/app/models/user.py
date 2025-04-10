#!/usr/bin/python3
import uuid
from app import db, bcrypt
from .base_model import BaseModel
from datetime import datetime
import re

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
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List to store places owned by the user

        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def add_place(self, place):
        """Add a place to the user's list of owned places."""
        if not isinstance(place, Place):
            raise ValueError("The provided place must be an instance of Place.")
        self.places.append(place)
