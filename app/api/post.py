from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from schema import Schema, And, Optional, SchemaError, Use
from datetime import datetime
from app.controllers.post import get_posts, add_post, get_post, delete_post
from app.controllers.user import get_user, is_authorized


bp = Blueprint('post_api', __name__)
api = Api(bp)

# son formatında veri alınır ve kısıtlamalar getirildi.
# lamda anlık olusturulan format turudur.
CREATE_POST_SCHEMA = Schema({
    'title': And(str, lambda s: 0 < len(s) <= 50),
    'text': And(str, lambda s: len(s) > 0),
    'date': And(str, Use(lambda s: datetime.strptime(
        s, '%Y-%m-%d %H:%M:%S.%f'))),
    Optional('image'): str,
})


class Post(Resource):
    def get(self):
        try:
            post_id = int(request.args.get("id"))
        except:
            print("Gecersiz Post_id")
            abort(400)

        data = get_post(post_id)
        if not data:
            print("Bu post_id:{}'ye sahip post bulunamadi".format(post_id))
            abort(404)

        return {'status': 'OK',
                'data': data}

    def post(self):
        token = request.headers.get("X-Token")
        user = get_user(token)

        if not user:
            print("Boyle bir kullanici bulunamadi")
            abort(401)

        if user['rank'] not in (0, 1):
            print("Yetkisiz kullanici : {}".format(user['rank']))
            abort(403)

        try:
            data = CREATE_POST_SCHEMA.validate(request.json)
            # add user_id to dictionary
            data['user_id'] = user['id']
        except SchemaError:
            print("400 Geldi")
            abort(400)

        add_post(**data)
        return {'status': 'OK'}

    def delete(self):
        token = request.headers.get("X-Token")
        user = get_user(token)
        if not user:
            print("Boyle bir kullanici bulunamadi")
            abort(401)

        try:
            post_id = int(request.args.get("id"))
        except:
            print("Gecersiz Post_id")
            abort(400)

        if is_authorized(token, post_id):
            status = delete_post(post_id)
            if status:
                return {'status': 'OK'}
        abort(401)


class Posts(Resource):
    """docstring for Post"""
    def get(self):
        data = get_posts()
        return {'status': 'OK', 'data': data}

api.add_resource(Post, '/api/post')
api.add_resource(Posts, '/api/posts')
