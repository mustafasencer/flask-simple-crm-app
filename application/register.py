"""
    Created by Mustafa Sencer Özcan on 12.05.2020.
"""
from flask import (Blueprint, request)

from application import mongo, error_response
from application.utils import success_response, validate_schema, hash_md5, Dynamic

bp = Blueprint('register', __name__)


@bp.route('/contacts', methods=('POST',))
@validate_schema('register')
def register(schema):
    schema = Dynamic(schema)
    if not request.method == 'POST':
        return error_response('Please provide all the necessary information!', status=400)
    if mongo.contacts.find_one({'email': schema.email}):
        return error_response(f'A Contact already exists with this E-Mail: `{schema.email}`!', status=409)
    _hashed_password = hash_md5(schema.password)
    mongo.contacts.insert_one({
        'first_name': schema.first_name,
        'last_name': schema.last_name,
        'email': schema.email,
        'username': schema.username,
        'password': _hashed_password
    })
    return success_response(f'Contact registered successfully.')
