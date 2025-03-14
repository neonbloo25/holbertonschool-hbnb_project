from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository

class HBnBFacade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository(User)  # Switched to SQLAlchemyRepository
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repository.add(user)
        return user

    def get_user_by_id(self, user_id):
        return self.user_repository.get(user_id)

    def get_all_users(self):
        return self.user_repository.get_all()

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)
    
    """ This line details the stuff that comes after this is altered
            def function(self):
            #description line for placeholder
            pass
        ^^^this is how the placeholders used to look^^^ """

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repository.get(amenity_id)
        if amenity:
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
            self.amenity_repository.update(amenity)
        return amenity

    def create_place(self, place_data):
        if not isinstance(place_data.get('price'), (int, float)) or place_data['price'] <= 0:
            raise ValueError("Price must be a positive number.")
        
        if not (-90 <= place_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        
        if not (-180 <= place_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        
        place = Place(**place_data)
        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repository.get(place_id)
        if place:
            place.owner = self.user_repository.get(place.owner_id)
            place.amenities = self.amenity_repository.get_by_attribute('place_id', place_id)
        return place

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repository.get(place_id)
        if place:
            for key, value in place_data.items():
                setattr(place, key, value)
            self.place_repository.update(place)
        return place

    def create_review(self, review_data):
        if not review_data.get('user_id') or not review_data.get('place_id'):
            raise ValueError("Both user_id and place_id are required.")
        
        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        
        review = Review(**review_data)
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repository.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        review = self.review_repository.get(review_id)
        if review:
            for key, value in review_data.items():
                setattr(review, key, value)
            self.review_repository.update(review)
        return review

    def delete_review(self, review_id):
        review = self.review_repository.get(review_id)
        if review:
            self.review_repository.delete(review)
        return review
