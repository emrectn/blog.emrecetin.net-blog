from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from app.controllers.label import add_label, delete_label
from app.controllers.user import get_user
from app.controllers.post import delete_post


bp = Blueprint('label', __name__)
api = Api(bp)


def authorized_with_token(f):
    def func(*args, **kwargs):
        token = request.headers.get("X-Token")
        user = get_user(token)

        if not user:
            print("Boyle bir kullanici bulunamadi")
            abort(401)
        kwargs['user'] = user
        return f(*args, **kwargs)
    return func


class Label(Resource):

    @authorized_with_token
    def post(self, user):
        data = request.json.get("labels")
        post_id = request.json.get("post_id")

        if user['rank'] in (0, 1):

            add_label(data, post_id)
            return {'status': 'OK'}
        abort(401)

    @authorized_with_token
    def delete(self, user):
        label_id = request.args.get("label_id")
        status = delete_label(label_id)
        if status:
            return {'status': 'OK'}
        abort(400)


api.add_resource(Label, '/api/label')
