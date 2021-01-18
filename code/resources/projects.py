from models.project import ProjectModel
from flask_restful import Resource, reqparse
from models.project import ProjectModel
from models.user import UserModel
from models.task import TaskModel
from models.permission import PermissionModel
from models.shareproject import ShareProjectModel
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, and_
from validations import non_empty_string


class Project(Resource):

    @jwt_required
    def get(self, name):
        project = ProjectModel.find_by_name(name)
        if project:
            return {"project": project.json(), "status": 200}

        return {
            "ProjectNotExistsError": {
                "message": "Project with given name doesn't exists",
                "status": 400,
            }}

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
        project_parse.add_argument('project_color_identity',
                                   type=non_empty_string,
                                   required=True,
                                   help="project_color_identity is required")

        project = ProjectModel.find_by_name(name)
        if project:
            return {
                "ProjectAlreadyExistsError": {
                    "message": "Project with given name already exists",
                    "status": 400
                }}

        data = project_parse.parse_args()
        project = ProjectModel(data['name'], data['description'],
                               get_jwt_identity(), data['project_color_identity'])
        project.save_to_db()
        return {"message": "Project Created", "status": 200}

    @jwt_required
    def put(self, name):
        project_parse = reqparse.RequestParser()
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
            if project.created_by_id == get_jwt_identity():
                # owner can do anything
                project.description = data['description']
                if data['permission'] != None:
                    project.permissions = data['permission']

                if data['name'] != None:
                    project.name = data['name']

                project.save_to_db()
                return {"Message": "Project Updated..", "status": 200}
            else:
                # not owner but have permission to edit

                collaborator = ShareProjectModel.query.filter(
                    and_(ShareProjectModel.share_with_id == get_jwt_identity(), ShareProjectModel.uuid == project.uuid)).first()

                if collaborator:
                    if collaborator.permission == "Edit" or collaborator.permission == "Delete":
                        project.description = data['description']
                        project.save_to_db()
                        return {
                            "message":
                            "Project Details Updated..",
                            "Note":
                            "You are part of this project not Owner.",
                            "status": 200
                        }

                    # no permission to update
                    return {
                        "UpdatingProjectError": {
                            "message": "You don't have Edit permission",
                            "status": 401,
                            "id":  get_jwt_identity(),
                            "coll": collaborator.permission
                        }}

                return {
                    "CollaboratorNotExistsError": {
                        "message": "Collaborator with given id doesn't exists",
                        "status": 400
                    }}

        return {
            "ProjectNotExistsError": {
                "message": "Project with given name doesn't exists",
                "status": 400
            }}

    @jwt_required
    def delete(self, name):
        project = ProjectModel.find_by_name(name)
        project_parse = reqparse.RequestParser()
        data = project_parse.parse_args()
        if project:
            if project.created_by_id == get_jwt_identity():
                # owner can do anything
                project.delete_from_db()
                return {"message": "Project Deleted..", "status": 200}
            else:
                # not owner but have a permission to delete
                collaborator = ShareProjectModel.query.filter(
                    and_(ShareProjectModel.share_with_id == get_jwt_identity(), ShareProjectModel.uuid == project.uuid)).first()

                if collaborator:
                    if collaborator.permission == "Delete":
                        project.delete_from_db()
                        return {"message": "Project Deleted.", "status": 200}

                    # no permission to update
                    return {
                        "DeletingProjectError": {
                            "message": "You don't have Delete permission",
                            "status": 401
                        }}
                return {
                    "CollaboratorNotExistsError": {
                        "message": "Collaborator with given id doesn't exists",
                        "status": 400
                    }}
        return {
            "ProjectNotExistsError": {
                "message": "Project with given name doesn't exists",
                "status": 400
            }}


class ProjectList(Resource):

    @jwt_required
    def get(self):
        # remaining task -> join user & project
        projects = [
            project.json() for project in ProjectModel.query.filter_by(
                created_by_id=get_jwt_identity()).all()
        ]

        share = [project.uuid for project in ShareProjectModel.query.filter_by(
            share_with_id=get_jwt_identity()).all()]

        Sharing_Projects = [
            ProjectModel.find_by_id(uuid).json() for uuid in share if ProjectModel.find_by_id(uuid) != None
        ]
        return {"Created Projects": projects, "Sharing_Projects": Sharing_Projects, "status": 200}


class AllProjectsList(Resource):

    def get(self):
        projects = [project.json() for project in ProjectModel.query.all()]
        return {"TotalProjects": len(projects), "Projects": projects, "status": 200}
