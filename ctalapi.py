# ctalapi.py

from flask import Blueprint, jsonify

cta_l_api = Blueprint('cta_l_api', __name__)

@cta_l_api.get("/ctalrides")
def get_countries():
    return jsonify({"stationname": "Addison/Clark", "riders": 51})