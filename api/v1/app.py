#!/usr/bin/python3
"""Main application file for Flask project"""
import os

from flask import Flask
from flask import jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exceptions=None):
    """Remove current database session after each request"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=int(os.getenv("HBNB_API_PORT", default="5000")),
            threaded=True
            )
