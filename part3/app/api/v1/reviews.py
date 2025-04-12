#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from app.models.review import Review
from app.models.place import Place
from app.models.user import User

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        print("🔧 Creating a new review...")  # Debug
        review_data = request.json

        # Validate the review data
        user = facade.get_user(review_data['user_id'])
        place = facade.get_place(review_data['place_id'])

        if not user:
            print("❌ User not found.")  # Debug
            return {'error': 'User not found'}, 400
        if not place:
            print("❌ Place not found.")  # Debug
            return {'error': 'Place not found'}, 400

        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )

        facade.create_review(new_review)
        print(f"💾 Review successfully created for place {place.id}.")  # Debug
        return {'id': new_review.id, 'message': 'Review successfully created'}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        print("🔧 Fetching all reviews...")  # Debug
        reviews = facade.get_all_reviews()

        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        } for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        print(f"🔧 Fetching review details for review ID: {review_id}")  # Debug
        review = facade.get_review(review_id)
        if not review:
            print("❌ Review not found.")  # Debug
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id
        }
