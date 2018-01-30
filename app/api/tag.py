from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from app.controllers.tag import get_labels, add_label, get_label
from app.controllers.user import get_user


bp = Blueprint('tag', __name__)
api = Api(bp)


class Tag(Resource):
    def get(self):
        try:
            label_id = int(request.args.get("id"))
        except:
            print("Gecersiz label_id")
            abort(400)

        data = get_label(label_id)
        if not data:
            print("Bu label_id: {}'li etiket bulunamadi".format(label_id))
            abort(404)

        return {'status': 'OK',
                'data': data}

    def post(label_id):
        token = request.headers.get("X-Token")
        user = get_user(token)

        if not user:
            print("Boyle bir kullanici bulunamadi")
            abort(401)

        data = request.json.get("labels")
        post_id = request.json.get("post_id")

        add_label(data, post_id)
        return {'status', 'OK'}


class Tags(Resource):
    def get(self):
        data = get_labels()
        return {'status': 'OK',
                'data': data}


api.add_resource(Tag, '/api/tag')
api.add_resource(Tags, '/api/tags')