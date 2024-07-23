# ctalapi.py

from flask import Blueprint, jsonify

from models.ctal import CTAL

cta_l_api = Blueprint('cta_l_api', __name__)
ctal = CTAL()


@cta_l_api.get("/ctalrides")
def get_ctalrides():
    response = jsonify(ctal.getdata())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
