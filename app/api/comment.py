from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from schema import Schema, And, Optional, SchemaError, Use
from datetime import datetime
from string import ascii_lowercase, digits
from app.controllers.comment import get_article_comments, add_comment
from app.controllers.user import get_user


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

        try:
            data = CREATE_COMMENT_SCHEMA.validate(request.json)
            # add user_id to dictionary
            data['user_id'] = user['id']
            data['post_id'] = int(request.args.get("post_id"))

        except SchemaError:
            print("SchemaError")
            abort(400)

        except TypeError:
            print("Hatalı post id")
            abort(400)
        print('hello')
        status = add_comment(**data)

        if status:
            return{'status': 'OK'}
        abort(401)


api.add_resource(Comment, '/api/comment')