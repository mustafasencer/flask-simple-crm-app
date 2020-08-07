"""
    Created by Mustafa Sencer Özcan on 12.05.2020.
"""
from bson import ObjectId
from flask import (Blueprint)
from flask_jwt_simple import jwt_required

from application import mongo
from application.utils import success_response, validate_schema, error_response, hash_md5, Dynamic

bp = Blueprint('update', __name__)


@bp.route('/contacts/<cid>/reset-password', methods=('POST',))
@jwt_required
@validate_schema('reset-password')
def update_contact(schema, cid):
    schema = Dynamic(schema)
    _current_contact = mongo.contacts.find_one({'_id': ObjectId(cid)})
    if not _current_contact:
        return error_response(f'No contact with Id: `{cid}` ', 400)
    _hashed_new_password = hash_md5(schema.new_password)
    if _current_contact.get('password') == _hashed_new_password:
        return error_response('Please change your password. Your new password is the same as your current password.',
                              400)
    _id = mongo.contacts.update_one({'_id': ObjectId(cid)}, {"$set": {"password": _hashed_new_password}})
    return success_response('Contact password has been successfully changed!')
