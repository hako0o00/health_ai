
from __init__ import create_app
from flask import Flask, request, jsonify
from flask_cors import CORS

app = create_app()

CORS(app)
CORS(app, resources={r"/api/": {"origins": "*"}})

if __name__ == "__main__":
    app.run(debug=True)
