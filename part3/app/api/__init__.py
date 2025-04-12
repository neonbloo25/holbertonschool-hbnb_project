#!/usr/bin/python3
from flask_restx import Api
from flask import Blueprint
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.auth import api as auth_ns


def create_api():
    """API blueprints"""
    print("🔧 Creating API blueprint for v1...")  # Debug
    api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

    print("⚙️ Initializing Flask-RESTx API...")  # Debug
    api = Api(
        api_v1,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/docs'  # 👈 Enables Swagger UI at /api/v1/docs
    )

    print("📦 Registering namespaces...")  # Debug
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(amenities_ns, path='/amenities')
    api.add_namespace(places_ns, path='/places')

    print("✅ API blueprint ready.")  # Debug
    return api_v1
