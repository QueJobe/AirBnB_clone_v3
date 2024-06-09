#!/usr/bin/python3
"""access blueprint"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', methods=['GET'])
def get_status():
	"""Return status of api"""
	return jsonify({"Status": "Ok"})

@app_views.route('/status', methods=['GET'])
def get_stats():
	"""Retrieve number of each object"""
	stats = {
		"amenities": storage.count(Amenity),
		"cities": storage.count(City),
		"place": storage.count(Place),
		"review": storage.count(Review),
		"states": storage.count(State),
		"users": storage.count(User)
	}
	return jsonify(stats)

