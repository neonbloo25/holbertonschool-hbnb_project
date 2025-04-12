#!/usr/bin/python3
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.persistence.user_repository import UserRepository
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class HBnBFacade:
    def __init__(self):
        print("🔧 Initializing HBnBFacade...")  # Debug
        self.user_repo = UserRepository()
        print("✅ UserRepository initialized.")  # Debug

    def create_user(self, user_data):
        print(f"📦 Creating user with data: {user_data}")  # Debug
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        print(f"✅ User created: {user}")  # Debug
        return user

    def get_user(self, user_id):
        print(f"🔍 Retrieving user with ID: {user_id}")  # Debug
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        print(f"🔍 Retrieving user with email: {email}")  # Debug
        return self.user_repo.get_by_attribute('email', email)

    def create_amenity(self, amenity_data):
        print(f"📦 Creating amenity with data: {amenity_data}")  # Debug
        # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
        print(f"🔍 Retrieving amenity with ID: {amenity_id}")  # Debug
        # Placeholder for logic to retrieve an amenity by ID
        pass

    def get_all_amenities(self):
        print("📋 Retrieving all amenities...")  # Debug
        # Placeholder for logic to retrieve all amenities
        pass

    def update_amenity(self, amenity_id, amenity_data):
        print(f"♻️ Updating amenity {amenity_id} with data: {amenity_data}")  # Debug
        # Placeholder for logic to update an amenity
        pass

    def create_place(self, place_data):
        print(f"📦 Creating place with data: {place_data}")  # Debug
        # Placeholder for logic to create a place
        pass

    def get_place(self, place_id):
        print(f"🔍 Retrieving place with ID: {place_id}")  # Debug
        # Placeholder for logic to retrieve a place by ID
        pass

    def get_all_places(self):
        print("📋 Retrieving all places...")  # Debug
        # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
        print(f"♻️ Updating place {place_id} with data: {place_data}")  # Debug
        # Placeholder for logic to update a place
        pass

    def create_review(self, review_data):
        print(f"📦 Creating review with data: {review_data}")  # Debug
        # Placeholder for logic to create a review
        pass

    def get_review(self, review_id):
        print(f"🔍 Retrieving review with ID: {review_id}")  # Debug
        # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
        print("📋 Retrieving all reviews...")  # Debug
        # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
        print(f"🔍 Retrieving all reviews for place ID: {place_id}")  # Debug
        # Placeholder for logic to retrieve reviews for a place
        pass

    def update_review(self, review_id, review_data):
        print(f"♻️ Updating review {review_id} with data: {review_data}")  # Debug
        # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
        print(f"🗑️ Deleting review with ID: {review_id}")  # Debug
        # Placeholder for logic to delete a review
        pass
