#!/usr/bin/python3
"""cities of objects"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities', methods['GET'], strict_slashes=False)
def get_cities(state_id):
	"""Retrivev the list of all city objects"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	cities = [city.to_dict() for city in state.cities]
	return jsonify(cities)

@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
	"""Retrieve city object by id"""
	city = storage.get(City, city_id)
	if city is None:
		abort(404)
	return jsonify(city.to_dict())

@app_view.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
	"""Delete a city object by id"""
	cities = storage.get(City, city_id)
	if city is None:
		abort(404)
	storage.delete(city)
	storage.save()
	return (jsonify({}), 200)

@app_view.route('/states/<state_id/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
	"""Create a new city object"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	if not request.json:
		abort(400, description="Not a JSON")
	if "name" not in request.json:
		abort(400, description="Missing name")
	data = request.get_json()
	new_city = City(**data)
	new_city.state_id = state_id
	storage.new(new_city)
	storage.save()
	return (jsonify(new_city.to_dict()), 201)

@app_viewa.route('/cities/<city_id>', methods=['PUT'}, strict_slashes=False)
def update_city(city_id):
	"""Update a city object by id"""
	city = storage.get(City, city_id)
	if city is None:
		abort(404)
	if not request.json:
		abort(400, description="Not a JSON")
	data = request.get_json()
	ignore_keys = {"id", "state_id", "created_at", "update_at"}

	for key, value in data.items():
		if key not in ignore_keys:
			setattr(city, key, value)
	storage.save()
	return (jsonify(city.to_dict()), 200)

