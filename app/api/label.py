from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from app.controllers.label import add_label
from app.controllers.user import get_user


bp = Blueprint('label', __name__)
api = Api(bp)


class Label(Resource):

    def post(self):
        token = request.headers.get("X-Token")
        user = get_user(token)

        if not user:
            print("Boyle bir kullanici bulunamadi")
            abort(401)

        data = request.json.get("labels")
        post_id = request.json.get("post_id")

        if user['rank'] in (0, 1):
            add_label(data, post_id)
            return {'status': 'OK'}

        abort(401)


api.add_resource(Label, '/api/label')