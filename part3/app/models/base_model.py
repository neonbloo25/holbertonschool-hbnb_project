#!/usr/bin/python3
from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BaseModel:
    def __init__(self):
        print("🔧 Initializing BaseModel...")  # Debug
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        print(f"✅ BaseModel created with ID {self.id}")  # Debug

    def save(self):
        print(f"💾 Saving BaseModel with ID {self.id}...")  # Debug
        self.updated_at = datetime.now()
        print("✅ Save complete. Timestamp updated.")  # Debug

    def update(self, data):
        print(f"♻️ Updating BaseModel {self.id} with data: {data}")  # Debug
        for key, value in data.items():
            if hasattr(self, key):
                print(f"🔄 Setting {key} to {value}")  # Debug
                setattr(self, key, value)
        self.save()
