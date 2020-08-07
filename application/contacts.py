"""
    Created by Mustafa Sencer Özcan on 12.05.2020.
"""
from bson import ObjectId
from flask import (Blueprint)
from flask.json import jsonify, dumps, loads

from application import mongo, redis_client, error_response
from application.utils import hash_md5

bp = Blueprint('contacts', __name__)


@bp.route('/contacts', methods=('GET',))
def contacts():
    all_contacts = mongo.contacts.find({}, {'password': 0})
    return jsonify(all_contacts)


@bp.route('/contacts/<cid>', methods=('GET',))
def contact(cid):
    _hashed_id = hash_md5(cid)
    cached_value = redis_client.get(_hashed_id)
    if cached_value:
        return jsonify(loads(cached_value.decode()))
    selected_contact = mongo.contacts.find_one({'_id': ObjectId(cid)}, {'password': 0})
    if not selected_contact:
        return error_response(f'No contact with Id: `{cid}` ', 400)
    redis_client.set(_hashed_id, dumps(selected_contact), ex=300)
    return jsonify(selected_contact)
