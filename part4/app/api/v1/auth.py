#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade
import logging

api = Namespace('auth', description='Authentication operations')

# Set up logging for this file
logger = logging.getLogger(__name__)

# Model for login request body validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        print(f"🔧 Received login request for email: {credentials['email']}")

        user = facade.get_user_by_email(credentials['email'])

        if not user:
            print("⚠️ User not found, invalid credentials.")
            return {'error': 'Invalid credentials'}, 401

        print(f"🔒 Stored password hash: {user.password_hash}")

        if not user.verify_password(credentials['password']):
            print("⚠️ Incorrect password, invalid credentials.")
            return {'error': 'Invalid credentials'}, 401

        # Create JWT token
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        print(f"✅ Login successful for user {user.id}, JWT token created.")
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        print(f"🔧 Protected resource accessed by user {current_user['id']}")
        return {'message': f'Hello, user {current_user["id"]}'}, 200
