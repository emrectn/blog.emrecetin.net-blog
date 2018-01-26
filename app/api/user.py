from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from schema import Schema, And, Optional, SchemaError
from string import ascii_lowercase, digits
from app.controllers.user import get_user_without_token, create_user, get_user, inactive_user, change_password
import re

bp = Blueprint('user', __name__)
api = Api(bp)


# Format olusturma, sadece belirli bir formatı kabul eder
EMAIL_PATTERN = re.compile('[{}{}.]+@[{}]+.[{}]'.format(
    ascii_lowercase, digits, ascii_lowercase, ascii_lowercase))
ASCII_LOWERCASE = re.compile('[{} çşğıüö]+'.format(ascii_lowercase))


CREATE_USER_SCHEMA = Schema({
    'email': And(str, lambda s: 0 < len(s) <= 60, EMAIL_PATTERN.match),
    'password': And(str, lambda s: len(s) >= 4),
    'fullname': And(str, lambda s: 5 < len(s) <= 80, ASCII_LOWERCASE.match),
    Optional('userinfo'): str,
})


class User(Resource):
    def post(self):
        try:
            data = CREATE_USER_SCHEMA.validate(request.json)
        except SchemaError:
            print("SchemaError")
            abort(400)

        exists = get_user_without_token(data['email'], data['password'])
        if exists:
            print("Bu kullanici: {} zaten var".format(data['email']))
            abort(400)

        create_user(**data)
        return{'status': 'OK'}

    def delete(self):
        token = request.headers.get("X-Token")
        user = get_user(token)

        if not user:
            print("Boyle bir kullanici bulunamadi")
            abort(401)

        inactive_user(user['id'])
        return {'status': 'OK'}

    def put(self):
        token = request.headers.get("X-Token")
        password = request.args.get("password")
        user = get_user(token)

        if not user:
            print("Boyle bir kullanici bulunamadi-put")
            abort(401)
        change_password(user['id'], password)
        return{'status': 'OK'}
        return


api.add_resource(User, '/api/user')
