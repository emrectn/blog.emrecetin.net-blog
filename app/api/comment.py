from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from schema import Schema, And, SchemaError, Use
from datetime import datetime
from app.controllers.comment import (get_article_comments, get_user_comments,
                                     add_comment, is_owner, delete_comment,
                                     publish_comment)

from app.controllers.user import get_user, is_admin


bp = Blueprint('comment', __name__)
api = Api(bp)


CREATE_COMMENT_SCHEMA = Schema({
    'text': And(str, lambda s: len(s) > 0),
    'date': And(str, Use(lambda s: datetime.strptime(
        s, '%Y-%m-%d %H:%M:%S.%f')))
})


class Comment(Resource):
    """docstring for Comment"""
    def get(self):
        try:
            post_id = int(request.args.get("post_id"))
        except:
            print("Gecersiz Post_id")
            abort(400)

        data = get_article_comments(post_id)
        if data:
            return {'status': 'ok',
                    'data': data}
        abort(400)

    def post(self):
        token = request.headers.get("X-Token")
        user = get_user(token)

        if not user:
            print("Boyle bir kullanici bulunamadi")
            abort(401)

        if user['status'] != 0:
            print("Yetkisiz kullanici")
            abort(403)

        try:
            data = CREATE_COMMENT_SCHEMA.validate(request.json)
            # add user_id to dictionary
            data['user_id'] = user['id']
            data['post_id'] = int(request.args.get("post_id"))

        except SchemaError:
            print("SchemaError")
            abort(400)

        except ValueError or TypeError:
            print("Hatalı post id")
            abort(400)
        status = add_comment(**data)

        if status:
            return{'status': 'OK'}
        abort(401)

    def delete(self):
        token = request.headers.get("X-Token")
        user = get_user(token)

        if not user:
            print("Boyle bir kullanici bulunamadi")
            abort(401)

        try:
            comment_id = int(request.args.get("comment_id"))
        except TypeError or ValueError:
            print("Gecersiz comment_id")
            abort(400)

        if is_admin(token) or is_owner(user['id'], comment_id):
            status = delete_comment(comment_id)
            if status:
                return {'status': 'OK'}
        abort(401)

    def put(self):
        token = request.headers.get("X-Token")
        user = get_user(token)

        if not user:
            print("Boyle bir kullanici bulunamadi")
            abort(401)
        try:
            comment_id = int(request.args.get("comment_id"))
        except TypeError or ValueError:
            print("Gecersiz comment_id")
            abort(400)

        if is_admin(token):
            status = publish_comment(comment_id)
            if status:
                return {'status': 'OK'}
        abort(403)


class Comments(Resource):
    """docstring for Comments"""
    def get(self):
        try:
            user_id = int(request.args.get("user_id"))
        except:
            print("Gecersiz user_id")
            abort(400)

        data = get_user_comments(user_id)
        if data:
            return {'status': 'ok',
                    'data': data}
        abort(400)


api.add_resource(Comment, '/api/comment')
api.add_resource(Comments, '/api/comments')