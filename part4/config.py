#!/usr/bin/python3
import os

print("🔧 Loading base configuration...")  # Debug

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

print("⚙️ Setting up development configuration...")  # Debug

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

print("📦 Mapping available configurations...")  # Debug

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

print("✅ Configuration ready.")  # Debug
