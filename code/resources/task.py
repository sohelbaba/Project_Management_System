from models.task import TaskModel
from flask_restful import Resource, reqparse
from flask import jsonify
from models.project import ProjectModel
from models.shareproject import ShareProjectModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_
from validations import non_empty_string


class Task(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('uuid', type=non_empty_string,
                       required=True, help='uuid Required..')
    parse.add_argument('task_name',
                       type=non_empty_string,
                       required=False,
                       help='task name Required..')
    parse.add_argument('task_desc',
                       type=non_empty_string,
                       required=True,
                       help='task_desc Required..')

    @jwt_required
    def post(self, name):
        data = Task.parse.parse_args()
        project = ProjectModel.query.filter_by(uuid=data['uuid']).first()

        if project:
            if project.created_by_id == get_jwt_identity():
                # owner
                if TaskModel.find_by_name(name):
                    return {
                        "TaskAlreadyExistsError": {
                            "message": "Task with given name alredy exists.",
                            "status": 401
                        }}

                task = TaskModel(name, data['task_desc'], data["uuid"])
                task.save_to_db()
                project = ProjectModel.find_by_id(data['uuid'])
                project.task_id = task
                project.save_to_db()
                return {"Message": "Task Added...", "status": 200}
            else:
                return {
                    "UnauthorizedError": {
                        "message": "Project Owner can only create task.",
                        "status": 401
                    }}

        return{
            "ProjectNotExistsError": {
                "message": "Project with given id doesn't exists",
                "status": 400
            }}

    @jwt_required
    def get(self, name):

        task = TaskModel.find_by_name(name)
        if task:
            return task.json()
        return {
            "TaskNotExistsError": {
                "message": "Task with given name doesn't exists",
                "status": 400
            }}

    @jwt_required
    def put(self, name):

        data = Task.parse.parse_args()
        project = ProjectModel.query.filter_by(uuid=data['uuid']).first()

        if project:
            task = TaskModel.query.filter(
                and_(TaskModel.uuid == data['uuid'],
                     TaskModel.task_name == name)).first()
            if task:
                if project.created_by_id == get_jwt_identity():
                    # owner
                    task.description = data['task_desc']
                    task.save_to_db()
                    return {"Message": "Task Edited", "status": 200}

                else:

                    collaborator = ShareProjectModel.query.filter(
                        and_(ShareProjectModel.share_with_id == get_jwt_identity(), ShareProjectModel.uuid == project.uuid)).first()

                    if collaborator:
                        if collaborator.permission == 'Edit' or collaborator.permission == 'Delete':
                            # share with permission to delete
                            task.description = data['task_desc']
                            task.save_to_db()
                            return {"Message": "Task Edited", "status": 200}

                        return {
                            "UnauthorizedError": {
                                "message": "You don't have permission to Edit Task.",
                                "status": 401
                            }}
                    return {
                        "CollaboratorNotExistsError": {
                            "message": "User with given id is not a part of this project or not owner",
                            "status": 400
                        }}

            return {
                "TaskNotExistsError": {
                    "message": "Task with given name doesn't exists",
                    "status": 400
                }}

        return {
            "ProjectNotExistsError": {
                "message": "Project with given id doesn't exists",
                "status": 400
            }}

    @jwt_required
    def delete(self, name):
        # user id,project id,task_name
        parse = reqparse.RequestParser()
        parse.add_argument('uuid',
                           type=non_empty_string,
                           required=True,
                           help='uuid Required..')

        data = parse.parse_args()

        project = ProjectModel.find_by_id(data['uuid'])
        if project:
            task = TaskModel.query.filter(
                and_(TaskModel.uuid == data['uuid'],
                     TaskModel.task_name == name)).first()
            if task:
                if project.created_by_id == get_jwt_identity():
                    # owner
                    task.delete_from_db()
                    return {"Message": "Task Deleted", "status": 200}

                else:
                    collaborator = ShareProjectModel.query.filter(
                        and_(ShareProjectModel.share_with_id == get_jwt_identity(), ShareProjectModel.uuid == project.uuid)).first()

                    if collaborator:
                        if collaborator.permission == 'Delete':
                            # share with permission to delete
                            task.delete_from_db()
                            return {"Message": "Task Deleted", "status": 200}
                        return {
                            "UnauthorizedError": {
                                "message": "You don't have permission to Delete Task.",
                                "status": 401
                            }}
                    return {
                        "CollaboratorNotExistsError": {
                            "message": "User with given id is not a part of this project or not owner",
                            "status": 400
                        }}

            return {
                "TaskNotExistsError": {
                    "message": "Task with given name doesn't exists",
                    "status": 400
                }}
        return {
            "ProjectNotExistsError": {
                "message": "Project with given id doesn't exists",
                "status": 400
            }}


class TaskList(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('uuid', type=str, required=True, help='uuid Required..')

    def get(self):
        data = TaskList.parse.parse_args()
        tasks = [
            task.json()
            for task in TaskModel.query.filter_by(uuid=data['uuid'])
        ]
        return {"Tasks": tasks, "status": 200}


class AllTaskList(Resource):
    def get(self):
        tasks = [task.json() for task in TaskModel.query.all()]
        return {"TotalTasks": len(tasks), "Tasks": tasks, "status": 200}
