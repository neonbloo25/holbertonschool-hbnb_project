#!/usr/bin/python3
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    print("🔧 Starting Flask app creation...")
    app = Flask(__name__)
    app.config.from_object(config_class)

    print("⚙️ Initializing extensions...")
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    print("📦 Registering blueprints...")
    from app.api import create_api
    api_blueprint = create_api()
    print(f"✅ Blueprint created: {api_blueprint}")
    app.register_blueprint(api_blueprint)

    print("🚀 Flask app ready to run.")
    return app
