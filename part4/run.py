#!/usr/bin/python3
from app import create_app

print("🔧 Creating the Flask app...")  # Debug

app = create_app()

print("✅ Flask app created.")  # Debug

if __name__ == '__main__':
    print("🚀 Running the Flask app...")  # Debug
    app.run(debug=True)
