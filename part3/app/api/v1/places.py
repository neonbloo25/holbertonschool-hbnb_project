#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.models import Place
import logging

api = Namespace('places', description='Place operations')

# Set up logging for this file
logger = logging.getLogger(__name__)

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        print(f"🔧 Received payload for new place: {place_data}")

        owner = facade.get_user(place_data['owner_id'])
        if not owner:
            print(f"⚠️ Owner with ID {place_data['owner_id']} not found.")
            return {'error': 'Owner not found'}, 400

        new_place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )
        facade.create_place(new_place)

        print(f"✅ Place with ID {new_place.id} created successfully.")
        return {'id': new_place.id, 'message': 'Place successfully created'}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        print("🔧 Fetching all places from the database.")
        places = facade.get_all_places()

        places_data = [{
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'owner': place.owner.to_dict(),
            'amenities': [amenity.to_dict() for amenity in place.amenities],
            'reviews': [review.to_dict() for review in place.reviews]
        } for place in places]

        print(f"✅ Returning {len(places_data)} places.")
        return places_data, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        print(f"🔧 Fetching place with ID {place_id}")
        place = facade.get_place(place_id)

        if not place:
            print(f"⚠️ Place with ID {place_id} not found.")
            return {'error': 'Place not found'}, 404

        print(f"✅ Returning details for place with ID {place_id}")
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'owner': place.owner.to_dict(),
            'amenities': [amenity.to_dict() for amenity in place.amenities],
            'reviews': [review.to_dict() for review in place.reviews]
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        print(f"🔧 User {current_user['id']} attempting to update place {place_id}")

        place = facade.get_place(place_id)

        if not place:
            print(f"⚠️ Place with ID {place_id} not found.")
            return {'error': 'Place not found'}, 404

        if place.owner_id != current_user['id']:
            print(f"⚠️ User {current_user['id']} is not authorized to update place {place_id}.")
            return {'error': 'Unauthorized action'}, 403

        updated_data = api.payload
        updated_place = facade.update_place(place_id, updated_data)

        print(f"✅ Place with ID {place_id} updated successfully.")
        return updated_place.to_dict(), 200
