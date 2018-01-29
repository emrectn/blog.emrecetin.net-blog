from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from schema import Schema, And, Optional, SchemaError
from string import ascii_lowercase, digits
from app.controllers.user import create_user, get_user, inactive_user, change_password, get_user_with_credentials
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


def authorized_with_token(f):
    def func(*args, **kwargs):
        token = request.headers.get("X-Token")
        user = get_user(token)
        if not user:
            print("Gecersiz Token, boyle bir kullanici bulunamadi")
            abort(401)
        # user keyword arguman olarak yollanılması gereklidir.
        # return f(user=user, *args, **kwargs) diyerek 35 satır iptaledilebilir
        kwargs['user'] = user
        return f(*args, **kwargs)
    return func


def authorized_with_credentials(f):
    def func(*args, **kwargs):
        try:
            data = CREATE_USER_SCHEMA.validate(request.json)
        except SchemaError:
            print("Gecersiz Veri seti schema Error")
            abort(403)

        exists = get_user_with_credentials(data['email'], data['password'])
        if exists:
            print("Bu kullanici: {} zaten var".format(data['email']))
            abort(400)

        kwargs['data'] = data
        return f(*args, **kwargs)
    return func


class User(Resource):

    @authorized_with_credentials
    def post(self, data):
        create_user(**data)
        return{'status': 'OK'}

    @authorized_with_token
    def delete(self, user):
        if user['status'] != 3:
            inactive_user(user['id'])
            return {'status': 'OK'}
        print('kullanici zaten silinmiş')
        abort(400)

    @authorized_with_token
    def put(self, user):
        new_password = request.json.get("new_password")
        old_password = request.json.get("old_password")

        status = change_password(user['id'], new_password, old_password)
        if not status:
            print("Sifre degistirilemedi")
            abort(401)
        return{'status': 'OK'}

api.add_resource(User, '/api/user')
