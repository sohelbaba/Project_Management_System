from models.project import ProjectModel
from flask_restful import Resource, reqparse
from models.project import ProjectModel
from models.user import UserModel
from models.task import TaskModel
from models.permission import PermissionModel
from models.shareproject import ShareProjectModel
from flask import jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from validations import non_empty_string


class Project(Resource):

    @jwt_required
    def get(self, name):
        project = ProjectModel.find_by_name(name)
        if project:
            return jsonify({"project": project.json(), "value": 200})
        return jsonify({"Message": "Project Not Found", "value": 404})

    @jwt_required
    def post(self, name):
        project_parse = reqparse.RequestParser()
        project_parse.add_argument('name',
                                   type=non_empty_string,
                                   required=True,
                                   help='Name is required')
        project_parse.add_argument('description',
                                   type=non_empty_string,
                                   required=True,
                                   help="description is required")
        project_parse.add_argument('created_by_id',
                                   type=non_empty_string,
                                   required=True,
                                   help="created_by_id is required")

        project = ProjectModel.find_by_name(name)
        if project:
            return jsonify({
                "Message":
                "Project with this name alredy Exists. Provide Unique Name.",
                "value": 401
            })

        data = project_parse.parse_args()
        project = ProjectModel(data['name'], data['description'],
                               data['created_by_id'])
        project.save_to_db()
        return jsonify({"Message": "Project Created", "value": 200})

    @jwt_required
    def put(self, name):
        project_parse = reqparse.RequestParser()
        project_parse.add_argument('id',
                                   type=int,
                                   required=True,
                                   help="user id is required")
        project_parse.add_argument('description',
                                   type=non_empty_string,
                                   required=True,
                                   help="description is required")
        project_parse.add_argument('permission',
                                   type=non_empty_string,
                                   required=False)
        project_parse.add_argument('name',
                                   type=non_empty_string,
                                   required=False)

        data = project_parse.parse_args()
        project = ProjectModel.find_by_name(name)

        if project:
            if project.created_by_id == data['id']:
                # owner can do anything
                project.description = data['description']
                if data['permission'] != None:
                    project.permissions = data['permission']

                if data['name'] != None:
                    project.name = data['name']

                project.save_to_db()
                return jsonify({"Message": "Project Updated..", "value": 200})
            else:
                #not owner
                collaborator = ShareProjectModel.query.filter_by(
                    share_with_id=data['id']).first()
                if collaborator:
                    if collaborator.permission == "Edit" or collaborator.permission == "Delete":
                        project.description = data['description']
                        project.save_to_db()
                        return jsonify({
                            "Message":
                            "Project Details Updated..",
                            "Note":
                            "You are part of this project not Owner.",
                            "value": 200
                        })
                    # # no permission to update
                    return jsonify({
                        "Message":
                        "You Don't Have a Permission to Edit this Project Details. Contact to Project Owner.",
                        "value": 203
                    })  # 203 -> Non Authorized

                return jsonify({"Message": "Not Found.", "value": 404})
        return jsonify({"Message": "Project Not Found.", "value": 404})

    @jwt_required
    def delete(self, name):
        project = ProjectModel.find_by_name(name)
        project_parse = reqparse.RequestParser()
        project_parse.add_argument('id',
                                   type=int,
                                   required=True,
                                   help="user id is required")

        data = project_parse.parse_args()
        if project:
            if project.created_by_id == data['id']:
                # owner can do anything
                project.delete_from_db()
                return jsonify({"Message": "Project Deleted..", "value": 200})
            else:
                #not owner
                collaborator = ShareProjectModel.query.filter_by(
                    share_with_id=data['id']).first()
                if collaborator:
                    if collaborator.permission == "Delete":
                        project.delete_from_db()
                        return jsonify({"Message": "Project Deleted.", "value": 200})

                    # no permission to update
                    return jsonify({
                        "Message":
                        "You Don't Have a Permission to Delete this Project Details. Contact to Project Owner.",
                        "value": 203
                    })

                return jsonify({"Message": "Not Found.", "value": 404})
        return jsonify({"Message": "Project Not Found.", "value": 404})


class ProjectList(Resource):
    def get(self, id):
        # remaining task -> join user & project
        projects = [
            project.json() for project in ProjectModel.query.filter_by(
                created_by_id=id).all()
        ]

        share = [project.uuid for project in ShareProjectModel.query.filter_by(
            share_with_id=id).all()]

        Collaborators = [
            ProjectModel.find_by_id(uuid).json() for uuid in share if ProjectModel.find_by_id(uuid) != None
        ]
        return jsonify({"Created Projects": projects, "Collaborators": Collaborators, "value": 200})


class AllProjectsList(Resource):
    def get(self):
        projects = [project.json() for project in ProjectModel.query.all()]
        return jsonify({"Projects": projects, "value": 200})
