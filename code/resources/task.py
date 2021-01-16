from models.task import TaskModel
from flask_restful import Resource, reqparse
from flask import jsonify
from models.project import ProjectModel
from models.shareproject import ShareProjectModel
from flask_jwt_extended import jwt_required
from sqlalchemy import and_


class Task(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('uuid', type=str, required=True, help='uuid Required..')
    parse.add_argument('id', type=int, required=True, help='id Required..')
    parse.add_argument('task_name',
                       type=str,
                       required=False,
                       help='task name Required..')
    parse.add_argument('task_desc',
                       type=str,
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
                        "Please Provide unique name to each task."
                    })

                task = TaskModel(name, data['task_desc'], data["uuid"])
                task.save_to_db()
                project = ProjectModel.find_by_id(data['uuid'])
                project.task_id = task
                project.save_to_db()
                return jsonify({"Message": "Task Added..."})
            else:
                return jsonify({
                    "Message":
                    "You are not owner of this project. Owner can only able to create tasks."
                })

        return jsonify({"Message": "Project Not Found"})

    @jwt_required
    def get(self, name):

        task = TaskModel.find_by_name(name)
        if task:
            return jsonify({"Task": task.json()})
        return jsonify({"Message": "Task Not Found."})

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
                    return jsonify({"Message": "Task Edited"})

                else:

                    collaborator = ShareProjectModel.query.filter_by(
                        share_with_id=data['id']).first()

                    if collaborator.permission == 'Edit' or collaborator.permission == 'Delete':
                        # share with permission to delete
                        task.description = data['task_desc']
                        task.save_to_db()
                        return jsonify({"Message": "Task Edited"})
                    return jsonify(
                        {"Message": "You Don't Have Permission to Edit Task."})

            return jsonify({"Message": "Task Not Found."})

        return jsonify({"Message": "Project Not Found."})

    @jwt_required
    def delete(self, name):
        # user id,project id,task_name
        parse = reqparse.RequestParser()
        parse.add_argument('uuid',
                           type=str,
                           required=True,
                           help='uuid Required..')
        parse.add_argument('id', type=int, required=True, help='id Required..')

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
                    return jsonify({"Message": "Task Deleted"})

                else:
                    collaborator = ShareProjectModel.query.filter_by(
                        share_with_id=data['id']).first()

                    if collaborator.permission == 'Delete':
                        # share with permission to delete
                        task.delete_from_db()
                        return jsonify({"Message": "Task Deleted"})
                    return jsonify(
                        {"Message": "You Don't Have Permission to Delete Task."})
            return jsonify({"Message": "Task Not Found."})
        return jsonify({"Message": "Project Not Found"})


class TaskList(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('uuid', type=str, required=True, help='uuid Required..')

    def get(self):
        data = TaskList.parse.parse_args()
        tasks = [
            task.json()
            for task in TaskModel.query.all()
        ]
        return jsonify({"Tasks": tasks})
