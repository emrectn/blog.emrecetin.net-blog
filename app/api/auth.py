from flask import Blueprint, request, abort, session
from flask_restful import Api, Resource
from schema import Schema, And, SchemaError, Use
from string import ascii_lowercase, digits
from app.controllers.user import login
import re

bp = Blueprint('auth', __name__)
api = Api(bp)

# Format olusturma sadece belirli formatı kabul eder.
USERNAME_PATTERN = re.compile('[{}{}.]+@[{}]+.[{}]'.format(
    ascii_lowercase, digits, ascii_lowercase, ascii_lowercase))


CREATE_AUTH_SCHEMA = Schema({
    'email': And(str, lambda s: 0 < len(s) <= 60, USERNAME_PATTERN.match),
    'password': And(str, lambda s: len(s) > 4),
})


class Auth(Resource):
    def post(self):
        data = CREATE_AUTH_SCHEMA.validate(request.json)

        print('email {} password {}'.format(data['email'], data['password']))
        token = login(data['email'], data['password'])

        if not token:
            abort(401)

        return {'status': 'OK',
                'data': token}


api.add_resource(Auth, '/api/auth')
