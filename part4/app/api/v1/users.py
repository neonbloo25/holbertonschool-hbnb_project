#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services import facade
from app.models.user import User
from app.models.amenity import Amenity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        print("🔧 Registering a new user...")  # Debug
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            print("❌ Email already registered.")  # Debug
            return {'error': 'Email already registered'}, 400

        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password']
        )
        new_user.hash_password(user_data['password'])

        print("💾 Saving new user...")  # Debug
        facade.create_user(new_user)
        print(f"✅ User successfully created with ID: {new_user.id}")  # Debug
        return {'id': new_user.id, 'message': 'User successfully created'}, 201

@api.route('users/<user_id>')
class UserResource(Resource):
    @jwt_required
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        print(f"🔧 Fetching details for user ID: {user_id}")  # Debug
        user = facade.get_user(user_id)
        if not user:
            print("❌ User not found.")  # Debug
            return {'error': 'User not found'}, 404
        return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 200

api = Namespace('admin', description='Admin operations')

@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        
        print(f"🔧 Admin user {current_user.get('id')} trying to update user {user_id}")  # Debug
        if not current_user.get('is_admin'):
            print("❌ Admin privileges required.")  # Debug
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            print(f"🔍 Checking if email {email} is already in use...")  # Debug
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                print("❌ Email is already in use by another user.")  # Debug
                return {'error': 'Email is already in use'}, 400

        # Placeholder for further functionality
        pass

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        print(f"🔧 Admin {current_user.get('id')} trying to create a new user...")  # Debug
        if not current_user.get('is_admin'):
            print("❌ Admin privileges required.")  # Debug
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        print(f"🔍 Checking if email {email} is already registered...")  # Debug
        if facade.get_user_by_email(email):
            print("❌ Email already registered.")  # Debug
            return {'error': 'Email already registered'}, 400

        # Placeholder for further functionality
        pass
