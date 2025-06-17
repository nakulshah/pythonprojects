from flask import Blueprint, jsonify, request

mathapi = Blueprint('mathapi', __name__)

@mathapi.get('/mathapi/add/<int:a>/<int:b>')
def add(a, b):
    """Add two integers."""
    result = a + b
    response = jsonify({'result': result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

