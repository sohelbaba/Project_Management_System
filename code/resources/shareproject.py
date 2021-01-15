from models.project import ProjectModel
from flask_restful import Resource, reqparse
from models.project import ProjectModel
from models.user import UserModel
from models.shareproject import ShareProjectModel
from models.permission import PermissionModel
from flask import jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_


class ProjectShare(Resource):
    projectshare_parse = reqparse.RequestParser()
    projectshare_parse.add_argument('uuid',
                                    type=str,
                                    required=True,
                                    help='uuid is required')
    projectshare_parse.add_argument('share_with_id',
                                    type=int,
                                    required=True,
                                    help="share id is required")
    projectshare_parse.add_argument('permission_id',
                                    type=str,
                                    required=True,
                                    help="permission is required")

    def post(self):
        data = ProjectShare.projectshare_parse.parse_args()
        user = UserModel.query.filter_by(id=data['share_with_id']).first()

        if user == None:
            return jsonify({"Message": "User Not Found"})
        else:
            if user.status:
                project = ProjectModel.find_by_id(data['uuid'])
                if project:

                    if project.json()['created_by'] == data['share_with_id']:
                        return jsonify({
                            "Message":
                            "Owner cannot share a project with itself.."
                        })

                    share = ShareProjectModel(
                        data['uuid'], data['share_with_id'], data['permission_id'])
                    share.save_to_db()

                    return jsonify({
                        "Message": "Project Share successfull",
                        "Share with": data['share_with_id']
                    })

                return jsonify({"Message": "Project Not Found"})

            return jsonify({
                "Message":
                "User Is Not Active. you can't share Your project"
            })
