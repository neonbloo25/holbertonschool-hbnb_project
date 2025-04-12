from flask import Flask
from flask_restx import Api, Resource, fields

print("🔧 Initializing Flask app...")  # Debug

app = Flask(__name__)
api = Api(app, version="1.0", title="HBnB API", description="API for HBnB application")

print("⚙️ Setting up the API...")  # Debug
user_ns = api.namespace('users', description="User operations")

print("📦 Initializing the users database...")  # Debug
users_db = {}

if __name__ == "__main__":
    print("🚀 Running the Flask app...")  # Debug
    app.run(debug=True)
