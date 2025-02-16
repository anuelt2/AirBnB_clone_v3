#!/usr/bin/python3
"""Main application file for Flask project"""
import os

from flask import Flask

from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exceptions=None):
    """Removes current database session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=int(os.getenv("HBNB_API_PORT", default="5000")),
            threaded=True
            )
