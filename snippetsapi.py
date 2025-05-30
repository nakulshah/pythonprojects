from flask import Blueprint, jsonify, request

from snippets.add_bdate_numbers import BirthDateAddition
from snippets.reverse import Reverse

snippets = Blueprint('snippets', __name__)


@snippets.get('/snippets/helloworld')
def helloworld():
    response = jsonify('hello world!')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@snippets.get('/snippets/birthdateadd')
def birthdateadd():
    addBirthdateNumber = BirthDateAddition()
    birthdate = request.args.get('birthdate')
    response = jsonify(addBirthdateNumber.addBirthDateNumbers(birthdate).serialize())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@snippets.get('/snippets/reverse/<to_reverse>')
def reverse(to_reverse):
    rev = Reverse()
    rev.rev(to_reverse)
    return jsonify(rev.serialize())

@snippets.get('/snippets/concatenate/<first>/<second>')
def concatenate(first, second):
    result = first + second
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response