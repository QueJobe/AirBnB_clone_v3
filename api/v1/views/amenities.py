#!/usr/bin/python3
"""new view for amenities objects"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.routes('/amenities', methods=['GET'], strict_slashes=False)
def get_amenites():
	"""Retrieve list of amenites objects"""
	amenities = [amenity.to_dict() for amenity in storage.all(Amenity).value()]
	return jsonify(amenities)

@app_views.route('/amenites/<amentiy_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
	"""Retrives an amentiy object by id"""
	amenity = storage.get(Amenity, amenity_id)
	if amenity is None:
		abort(404)
	return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
	"""Delete an amenity object by id"""
	amenity = storage.get(Amenity, amenity_id)
	if amenity is None:
		abort(404)
	storage.delete(amenity)
	storage.save()
	return (jsonify({}), 200)

@app_viewa.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
	"""create a new amanity object"""
	if not request.json:
		abort(400, description="Not a JSON")
	if "name" not in request.json:
		abort(400, description="Missing name")
	data = request.get_json()
	new_amenity = Amenity(**data)
	storage.new(new_amenity)
	storage.save()
	return (jsonify(new_amenity.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
	"""Update am Amenity object by id"""
	amenity = storage.get(Amenity, amenity_id)
	if amenity is None:
		abort(404)
	if not request.json:
		abort(400, description="Not a JSON")
	data = request.get_json()
	ignore_keys = {"id", "created_id", "updated_id"}

	for key, value in data.items():
		if key not in ignore_keys:
			setattr(amenity, key, value)
	storage.save()
	return (jsonify(amenity.to_dict()), 200)

