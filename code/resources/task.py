from models.task import TaskModel
from flask_restful import Resource, reqparse
from flask import jsonify
from models.project import ProjectModel


class Task(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('uuid', type=str, required=True, help='uuid Required..')
    parse.add_argument('task_name',
                       type=str,
                       required=True,
                       help='task name Required..')
    parse.add_argument('task_desc',
                       type=str,
                       required=True,
                       help='task_desc Required..')

    def post(self):
        data = Task.parse.parse_args()
        task = TaskModel(data['task_name'], data['task_desc'])
        task.save_to_db()
        project = ProjectModel.find_by_id(data['uuid'])
        project.task_id = task
        project.uuid = data['uuid']
        project.save_to_db()
        return jsonify({"Message": "Task Added..."})


class TaskList(Resource):
    def get(self):
        tasks = [task.json() for task in TaskModel.query.filter_by()]
        return jsonify({"Tasks": tasks})
