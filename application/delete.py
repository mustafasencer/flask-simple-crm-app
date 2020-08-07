"""
    Created by Mustafa Sencer Özcan on 12.05.2020.
"""
from bson import ObjectId
from flask import (Blueprint)
from flask_jwt_simple import jwt_required

from application import mongo, redis_client
from application.utils import success_response, hash_md5, error_response

bp = Blueprint('delete', __name__)


@bp.route('/contacts/<id>', methods=('DELETE',))
@jwt_required
def delete_contact(id):
    _hashed_id = hash_md5(id)
    if redis_client.get(_hashed_id):
        redis_client.delete(_hashed_id)
    if not mongo.contacts.find_one({'_id': ObjectId(id)}):
        return error_response(f'No Contact with Id: `{id}`!', 400)
    mongo.contacts.delete_one({'_id': ObjectId(id)})
    return success_response('Contact successfully deleted!')
