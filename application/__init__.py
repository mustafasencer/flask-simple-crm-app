"""
    Created by Mustafa Sencer Özcan on 12.05.2020.
"""
import datetime
import traceback
from os import environ

from pymongo import MongoClient
from redis import Redis
from bson import ObjectId
from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from application.schemas import RegisterSchema, ResetPasswordSchema, LoginSchema
from application.utils import error_response

mongo = MongoClient(environ.get('MONGO_HOST'), port=int(environ.get('MONGO_PORT'))).local_blutv
redis_client = Redis(environ.get('REDIS_HOST'), port=int(environ.get('REDIS_PORT')))
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=["50 per minute"])


def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['JWT_ALGORITHM'] = 'HS512'
    app.config['JWT_DECODE_AUDIENCE'] = 'secure-api'
    app.config['JWT_IDENTITY_CLAIM'] = 'uid'
    app.config['JSON_AS_ASCII'] = False
    app.config['register'] = RegisterSchema
    app.config['reset-password'] = ResetPasswordSchema
    app.config['login'] = LoginSchema

    class CustomJSONEncoder(JSONEncoder):
        def default(self, o):
            try:
                if isinstance(o, datetime.datetime):
                    return o.isoformat() + 'Z'
                if isinstance(o, datetime.date):
                    return o.isoformat()
                if isinstance(o, ObjectId):
                    return str(o)
                iterable = iter(o)
            except TypeError:
                pass
            else:
                return list(iterable)
            return JSONEncoder.default(self, o)

    app.json_encoder = CustomJSONEncoder

    # Init modules
    CORS(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # Routes
    from . import login, register, contacts, delete, reset_password
    app.register_blueprint(login.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(contacts.bp)
    app.register_blueprint(delete.bp)
    app.register_blueprint(reset_password.bp)

    @jwt.expired_token_loader
    def my_expired_token_callback():
        return error_response('Token expired', 403)

    @jwt.unauthorized_loader
    def my_expired_token_callback(reason):
        return error_response('Token not found', 403)

    @app.errorhandler(404)
    def page_not_found(e):
        return error_response('Route not found', 404, extra=str(e))

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        return error_response(message=traceback.format_exc(), status=500, extra=str(e))

    return app
