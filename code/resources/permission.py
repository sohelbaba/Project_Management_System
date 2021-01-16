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
            return {"permission": permission.name}

        return {
            "PermissionExistsError": {
                "message": "Permission with given id doesn't exists",
                "status": 400
            }}

    def post(self):
        data = Permission.parse.parse_args()
        permisson = PermissionModel.query.filter_by(id=data['id']).first()
        if permisson:
            return {
                "PermissionAlreadyExistsError": {
                    "message": "Permission with given id already exists",
                    "status": 400
                }}

        permission = PermissionModel(data['name'], data['desc'])
        permission.save_to_db()
        return {"Message": "Permission Add..", "status": 200}
