from flask import Blueprint, jsonify, json

from snippets.add_bdate_numbers import BirthDateAddition

snippets = Blueprint('snippets', __name__)

@snippets.get('/snippets/helloworld')
def helloworld():
    response = jsonify('hello world!')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@snippets.get('/snippets/birthdateadd')
def birthdateadd():
    addBirthdateNumber = BirthDateAddition()
    response = jsonify(addBirthdateNumber.addBirthDateNumbers('08/07/1984').serialize())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
