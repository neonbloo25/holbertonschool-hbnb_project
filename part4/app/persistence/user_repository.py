#!/usr/bin/python3
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        print("🔧 Initializing UserRepository...")  # Debug
        super().__init__(User)
        print("✅ UserRepository initialized with User model.")  # Debug

    def get_user_by_email(self, email):
        print(f"🔍 Querying user by email: {email}")  # Debug
        return self.model.query.filter_by(email=email).first()
