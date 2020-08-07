"""
    Created by Mustafa Sencer Özcan on 12.05.2020.
"""
from datetime import timedelta, datetime

from flask import (Blueprint, jsonify)
from flask_jwt_simple import create_jwt

from application import jwt, limiter, error_response, mongo
from application.utils import hash_md5, validate_schema, Dynamic

bp = Blueprint('login', __name__)


@bp.route('/login', methods=('POST',))
@limiter.limit("5 per minute")
@validate_schema('login')
def login(schema):
    schema = Dynamic(schema)
    _hashed_password = hash_md5(schema.password)
    contact = mongo.contacts.find_one({'email': schema.email, 'password': _hashed_password})
    if not contact:
        return error_response('Wrong Credentials. Please check your credentials.', 401)
    identity = {
        'uid': str(contact.get('_id')),
        'email': schema.email
    }
    access_token = create_jwt(identity=identity)
    return jsonify({'success': True, 'access_token': access_token})


@jwt.jwt_data_loader
def add_claims_to_access_token(identity):
    now = datetime.utcnow()
    expire_time = now + timedelta(minutes=20)
    uid = identity.pop('uid')
    return {
        'exp': expire_time,
        'iat': now,
        'nbf': now,
        'sub': identity,
        'uid': uid,
        'aud': 'secure-api',
    }
