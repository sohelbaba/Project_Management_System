from models.project import ProjectModel
from flask_restful import Resource, reqparse
from models.project import ProjectModel
from models.user import UserModel
from flask import jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_


class Project(Resource):
    project_parse = reqparse.RequestParser()
    project_parse.add_argument('name',
                               type=str,
                               required=True,
                               help='Name is required')
    project_parse.add_argument('description',
                               type=str,
                               required=True,
                               help="description is required")
    project_parse.add_argument('created_by_id',
                               type=str,
                               required=True,
                               help="created_by_id is required")

    @jwt_required
    def get(self, name):
        project = ProjectModel.find_by_name(name)
        if project:
            return project.json()
        return jsonify({"Message": "Project Not Found"})

    @jwt_required
    def post(self, name):
        project = ProjectModel.find_by_name(name)
        if project:
            return jsonify({
                "Message":
                "Project with this name alredy Exists. Provide Unique Name."
            })

        data = Project.project_parse.parse_args()
        project = ProjectModel(data['name'], data['description'],
                               data['created_by_id'])
        project.save_to_db()
        return {"Message": "Project Created"}

    @jwt_required
    def put(self):
        pass

    @jwt_required
    def delete(self):
        pass


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

    #@jwt_required
    def put(self):
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

                    project.share_with_id = data['share_with_id']
                    project.permissions = data['permission_id']
                    project.save_to_db()

                    return jsonify({
                        "Message": "Project Share successfull",
                        "Share with": data['share_with_id']
                    })
                return jsonify({"Message": "Project Not Found"})

            return jsonify({
                "Message":
                "User Is Not Active. you can't share Your project"
            })


class ProjectList(Resource):
    def get(self, id):
        #remaining task -> join user & project
        projects = [
            project.json() for project in ProjectModel.query.filter_by(
                created_by_id=id).all()
        ]
        if len(projects) == 0:
            share_projects = [
                project.json() for project in ProjectModel.query.filter_by(
                    share_with_id=id).all()
            ]
            return jsonify({"Shared_Projects": share_projects})

        return jsonify({"Projects": projects})
