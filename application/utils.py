"""
    Created by Mustafa Sencer Özcan on 12.05.2020.
"""
from functools import wraps
from hashlib import md5

from flask import (
    current_app,
    jsonify,
    request,
)
from marshmallow import ValidationError


def hash_md5(value):
    return md5(value.encode('utf-8')).hexdigest()


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                schema = current_app.config[schema_name]
                result = schema().load(data=request.json)
            except ValidationError as ex:
                return error_response('Validation Error', 400, ex.messages)
            return f(result, *args, **kw)

        return wrapper

    return decorator


class Dynamic(dict):
    def __setattr__(self, key, value):
        return super().__setitem__(key, value)

    def __getattr__(self, item):
        if item in self:
            value = super().__getitem__(item)
            if isinstance(value, dict):
                return Dynamic(value)
            return value
        return None

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, state):
        return Dynamic(state)


def success_response(message):
    return jsonify({"code": 200, "success": {"isSuccess": True, "message": message}}), 200


def error_response(message, status, extra=None):
    return jsonify(error={"message": message, "extra": extra}, code=status), status
