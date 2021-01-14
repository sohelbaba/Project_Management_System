from models.task import TaskModel
from flask_restful import Resource, reqparse
from flask import jsonify
from models.project import ProjectModel
from flask_jwt_extended import jwt_required


class Task(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('uuid', type=str, required=True, help='uuid Required..')
    parse.add_argument('id', type=int, required=True, help='id Required..')
    parse.add_argument('task_name',
                       type=str,
                       required=True,
                       help='task name Required..')
    parse.add_argument('task_desc',
                       type=str,
                       required=True,
                       help='task_desc Required..')

    @jwt_required
    def post(self, id):
        data = Task.parse.parse_args()
        project = ProjectModel.query.filter_by(uuid=data['uuid']).first()

        if project:
            if project.json()["created_by"] == data["id"]:
                #owner
                task = TaskModel(data['task_name'], data['task_desc'],
                                 data["uuid"])
                task.save_to_db()
                project = ProjectModel.find_by_id(data['uuid'])
                project.task_id = task
                project.uuid = data['uuid']
                project.save_to_db()
                return jsonify({"Message": "Task Added..."})
            else:
                return jsonify({
                    "Message":
                    "You are not owner of this project. Owner can only able to create tasks."
                })

        return jsonify({"Message": "Project Not Found"})


class TaskList(Resource):
    def get(self):
        tasks = [task.json() for task in TaskModel.query.filter_by()]
        return jsonify({"Tasks": tasks})
