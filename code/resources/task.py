from models.task import TaskModel
from flask_restful import Resource, reqparse
from flask import jsonify
from models.project import ProjectModel
from models.shareproject import ShareProjectModel
from flask_jwt_extended import jwt_required
from sqlalchemy import and_
from validations import non_empty_string


class Task(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('uuid', type=non_empty_string,
                       required=True, help='uuid Required..')
    parse.add_argument('id', type=non_empty_string,
                       required=True, help='id Required..')
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
            if project.created_by_id == data["id"]:
                # owner
                if TaskModel.find_by_name(name):
                    return jsonify({
                        "Message":
                        "Please Provide unique name to each task.",
                        "value": 401
                    })

                task = TaskModel(name, data['task_desc'], data["uuid"])
                task.save_to_db()
                project = ProjectModel.find_by_id(data['uuid'])
                project.task_id = task
                project.save_to_db()
                return jsonify({"Message": "Task Added...", "value": 200})
            else:
                return jsonify({
                    "Message":
                    "You are not owner of this project. Owner can only able to create tasks.",
                    "value": 400
                })

        return jsonify({"Message": "Project Not Found", "value": 200})

    @jwt_required
    def get(self, name):

        task = TaskModel.find_by_name(name)
        if task:
            return jsonify({"Task": task.json()})
        return jsonify({"Message": "Task Not Found.", "value": 200})

    @jwt_required
    def put(self, name):

        data = Task.parse.parse_args()
        project = ProjectModel.query.filter_by(uuid=data['uuid']).first()

        if project:
            task = TaskModel.query.filter(
                and_(TaskModel.uuid == data['uuid'],
                     TaskModel.task_name == name)).first()
            if task:
                if project.created_by_id == data['id']:
                    # owner
                    task.description = data['task_desc']
                    task.save_to_db()
                    return jsonify({"Message": "Task Edited", "value": 200})

                else:

                    collaborator = ShareProjectModel.query.filter_by(
                        share_with_id=data['id']).first()

                    if collaborator.permission == 'Edit' or collaborator.permission == 'Delete':
                        # share with permission to delete
                        task.description = data['task_desc']
                        task.save_to_db()
                        return jsonify({"Message": "Task Edited", "value": 200})
                    return jsonify(
                        {"Message": "You Don't Have Permission to Edit Task.", "value": 400})

            return jsonify({"Message": "Task Not Found.", "value": 404})

        return jsonify({"Message": "Project Not Found.", "value": 404})

    @jwt_required
    def delete(self, name):
        # user id,project id,task_name
        parse = reqparse.RequestParser()
        parse.add_argument('uuid',
                           type=non_empty_string,
                           required=True,
                           help='uuid Required..')
        parse.add_argument('id', type=non_empty_string,
                           required=True, help='id Required..')

        data = parse.parse_args()

        project = ProjectModel.find_by_id(data['uuid'])
        if project:
            task = TaskModel.query.filter(
                and_(TaskModel.uuid == data['uuid'],
                     TaskModel.task_name == name)).first()
            if task:
                if project.created_by_id == data['id']:
                    # owner
                    task.delete_from_db()
                    return jsonify({"Message": "Task Deleted", "value": 200})

                else:
                    collaborator = ShareProjectModel.query.filter_by(
                        share_with_id=data['id']).first()

                    if collaborator.permission == 'Delete':
                        # share with permission to delete
                        task.delete_from_db()
                        return jsonify({"Message": "Task Deleted", "value": 200})
                    return jsonify(
                        {"Message": "You Don't Have Permission to Delete Task.", "value": 400})
            return jsonify({"Message": "Task Not Found.", "value": 404})
        return jsonify({"Message": "Project Not Found", "value": 404})


class TaskList(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('uuid', type=str, required=True, help='uuid Required..')

    def get(self):
        data = TaskList.parse.parse_args()
        tasks = [
            task.json()
            for task in TaskModel.query.all()
        ]
        return jsonify({"Tasks": tasks, "value": 200})
