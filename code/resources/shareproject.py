from models.project import ProjectModel
from flask_restful import Resource, reqparse
from models.project import ProjectModel
from models.user import UserModel
from models.shareproject import ShareProjectModel
from models.permission import PermissionModel
from flask import jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from validations import non_empty_string


class ProjectShare(Resource):
    projectshare_parse = reqparse.RequestParser()
    projectshare_parse.add_argument('id',
                                    type=non_empty_string,
                                    required=True,
                                    help='id is required')
    projectshare_parse.add_argument('uuid',
                                    type=non_empty_string,
                                    required=True,
                                    help='uuid is required')
    projectshare_parse.add_argument('share_with_id',
                                    type=non_empty_string,
                                    required=True,
                                    help="share id is required")
    projectshare_parse.add_argument('permission',
                                    type=non_empty_string,
                                    required=True,
                                    help="permission is required")

    def post(self):
        data = ProjectShare.projectshare_parse.parse_args()
        user = UserModel.query.filter_by(id=data['share_with_id']).first()

        if user == None:
            return jsonify({"Message": "User Not Found", "value": 404})
        else:
            if user.status:
                project = ProjectModel.find_by_id(data['uuid'])
                if project:
                    if project.created_by_id == data['id']:
                        if project.json()['created_by'] == data['share_with_id']:
                            return jsonify({
                                "Message":
                                "Owner cannot share a project with itself.."
                            })
                        else:
                            permission = PermissionModel.find_by_name(
                                data['permission'])
                            if permission:
                                share = ShareProjectModel(
                                    data['uuid'], data['share_with_id'], data['permission'])
                                share.save_to_db()

                                return jsonify({
                                    "Message": "Project Share successfull",
                                    "Share with": user.name
                                })
                            return jsonify({"Message": "Enter permission is not Found."})
                    return jsonify({"Message": "Owner can only allow to share projects.", "value": 203})
                return jsonify({"Message": "Project Not Found", "value": 404})

            return jsonify({
                "Message":
                "User Is Not Active. you can't share Your project",
                "value": 404
            })
