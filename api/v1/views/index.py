#!/usr/bin/python3
"""Defines index route for Flask application"""
from flask import jsonify

from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Returns status of API"""
    return jsonify({"status": "OK"})
