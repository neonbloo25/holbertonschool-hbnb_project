from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version="1.0", title="HBnB API", description="API for HBnB application")

user_ns = api.namespace('users', description="User operations")

users_db = {}

if __name__ == "__main__":
    app.run(debug=True)
