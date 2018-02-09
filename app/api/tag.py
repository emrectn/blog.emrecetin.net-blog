from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from app.controllers.tag import add_tag, delete_tag
from app.controllers.user import get_user
from app.controllers.post import delete_post


bp = Blueprint('tag_api', __name__)
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


class Tag(Resource):

    @authorized_with_token
    def post(self, user):
        data = request.json.get("tags")
        post_id = request.json.get("post_id")

        if user['rank'] in (0, 1):

            add_tag(data, post_id)
            return {'status': 'OK'}
        abort(401)

    @authorized_with_token
    def delete(self, user):
        tag_id = request.args.get("tag_id")
        status = delete_tag(tag_id)
        if status:
            return {'status': 'OK'}
        abort(400)


api.add_resource(Tag, '/api/tag')
