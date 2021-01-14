from models.project import ProjectModel
from flask_restful import Resource, reqparse
from models.project import ProjectModel
from models.user import UserModel
from flask import jsonify


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

    def get(self, name):
        project = ProjectModel.find_by_name(name)
        if project:
            return project.json()
        return jsonify({"Message": "Project Not Found"})

    def post(self, name):
        data = Project.project_parse.parse_args()
        project = ProjectModel(data['name'], data['description'],
                               data['created_by_id'])
        project.save_to_db()
        return {"Message": "Project Created"}

    def put(self):
        pass

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

    def put(self):
        data = ProjectShare.projectshare_parse.parse_args()
        project = ProjectModel.find_by_id(data['uuid'])
        project.share_with_id = data['share_with_id']
        project.permissions = data['permission_id']
        project.save_to_db()
        return jsonify({"Message": "Project Share successfull"})


class ProjectList(Resource):
    def get(self, id):
        #remaining task -> join user & project
        projects = [project.json() for project in ProjectModel.query.all()]
        return jsonify({"Projects": projects})
