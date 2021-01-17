from models.project import ProjectModel
from flask_restful import Resource, reqparse
from models.project import ProjectModel
from models.user import UserModel
from models.shareproject import ShareProjectModel
from models.permission import PermissionModel
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from validations import non_empty_string


class ProjectShare(Resource):
    projectshare_parse = reqparse.RequestParser()
    projectshare_parse.add_argument('uuid',
                                    type=non_empty_string,
                                    required=True,
                                    help='uuid is required')
    projectshare_parse.add_argument('share_with_id',
                                    type=int,
                                    required=True,
                                    help="share id is required")
    projectshare_parse.add_argument('permission',
                                    type=non_empty_string,
                                    required=True,
                                    help="permission is required")

    @jwt_required
    def post(self):
        data = ProjectShare.projectshare_parse.parse_args()
        user = UserModel.query.filter_by(id=data['share_with_id']).first()

        if user == None:
            return {
                "UserNotExistsError": {
                    "message": "User with given id doesn't exists",
                    "status": 400
                }}
        else:
            if user.status:
                project = ProjectModel.find_by_id(data['uuid'])
                if project:
                    if project.created_by_id == get_jwt_identity():
                        if project.created_by_id == data['share_with_id']:
                            return {
                                "SharingProjectError": {
                                    "message": "You don't Share Project itself.",
                                    "status": 401
                                }}
                        else:
                            permission = PermissionModel.find_by_name(
                                data['permission'])
                            if permission:
                                share = ShareProjectModel(
                                    data['uuid'], data['share_with_id'], data['permission'])
                                share.save_to_db()

                                return{
                                    "Message": "Project Share successfull",
                                    "Share with": user.name
                                }
                            return {
                                "PermissionError": {
                                    "message": "permission not found",
                                    "status": 401
                                }}
                    return {
                        "SharingProjectError": {
                            "message": "You don't have Sharing permission",
                            "status": 401
                        }}
                return {
                    "ProjectNotExistsError": {
                        "message": "Project with given name doesn't exists",
                        "status": 400
                    }}

            return {
                "UserNotActiveError": {
                    "message": "User with give id is not Active.",
                    "status": 401
                }}
