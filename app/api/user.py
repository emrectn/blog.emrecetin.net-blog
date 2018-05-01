from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from schema import Schema, And, Optional, SchemaError
from string import ascii_lowercase, digits
from app.controllers.user import (create_user, get_user, inactive_user,
                                  change_password, make_admin)
import re

bp = Blueprint('user_api', __name__)
api = Api(bp)


# Format olusturma, sadece belirli bir formatı kabul eder
EMAIL_PATTERN = re.compile('[{}{}.]+@[{}]+.[{}]'.format(
    ascii_lowercase, digits, ascii_lowercase, ascii_lowercase))

CREATE_USER_SCHEMA = Schema({
    'email': And(str, lambda s: 0 < len(s) <= 60, EMAIL_PATTERN.match),
    'password': And(str, lambda s: len(s) >= 4),
    'fullname': And(str, lambda s: 5 < len(s) <= 80),
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


class User(Resource):

    def post(self):
        try:
            data = CREATE_USER_SCHEMA.validate(request.json)
        except SchemaError:
            print("Gecersiz Veri seti schema Error")
            abort(400)

        status = create_user(**data)
        if status:
            return{'status': 'OK'}
        abort(403)

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


class MakeAdmin(Resource):
    def put(self):
        username = request.json.get("username")
        token = request.json.get("token")
        status = make_admin(username, token)
        if status:
            return{'status': 'OK'}
        abort(400)
k
api.add_resource(User, '/api/user')
api.add_resource(MakeAdmin, '/api/makeadmin')
