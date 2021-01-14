from flask_restful import Resource, reqparse
from models.permission import PermissionModel
from flask import jsonify


class Permission(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('id', type=int, required=True, help='Id required')
    parse.add_argument('name', type=str, required=True, help='name required')
    parse.add_argument('desc', type=str, required=True, help='desc required')

    def get(self, id):
        permission = PermissionModel.query.filter_by(id=id).first()
        if permission:
            return jsonify({"permission": permission.name})

        return jsonify({"Message": "Incorrect Id"})

    def post(self):
        data = Permission.parse.parse_args()
        permisson = PermissionModel.query.filter_by(id=data['id']).first()
        if permisson:
            return jsonify({"Message": "Already added"})

        permission = PermissionModel(data['name'], data['desc'])
        permission.save_to_db()
        return jsonify({"Message": "Permission Add.."})
