#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
import logging

api = Namespace('amenities', description='Amenity operations')

# Set up logging for this file
logger = logging.getLogger(__name__)

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        print("🔧 Received request to create a new amenity.")
        amenity_data = api.payload
        print(f"🌱 Amenity name: {amenity_data['name']}")

        # Placeholder for the logic to register a new amenity
        pass

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        print("🔧 Fetching list of amenities...")
        # Placeholder for logic to return a list of all amenities
        pass


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        print(f"🔧 Fetching details for amenity with ID: {amenity_id}")
        # Placeholder for the logic to retrieve an amenity by ID
        pass

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        print(f"🔧 Received request to update amenity with ID: {amenity_id}")
        updated_data = api.payload
        print(f"🌱 New amenity data: {updated_data}")

        # Placeholder for the logic to update an amenity by ID
        pass


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        print(f"🔧 Admin user {current_user['id']} is trying to create a new amenity.")
        
        if not current_user.get('is_admin'):
            print("⚠️ Admin privileges required to create an amenity.")
            return {'error': 'Admin privileges required'}, 403

        # Placeholder for the logic to create a new amenity
        pass
