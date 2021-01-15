from config import db


class TaskModel(db.Model):

    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(250), unique=True)
    description = db.Column(db.Text)
    uuid = db.Column(db.Integer, db.ForeignKey('project.uuid'), default=None)

    def __init__(self, task_name, description, uuid):
        self.task_name = task_name
        self.description = description
        self.uuid = uuid

    def json(self):
        return {
            "task_name": self.task_name,
            "description": self.description,
            "uuid": self.uuid
        }

    @classmethod
    def find_by_name(cls, name):
        return TaskModel.query.filter_by(task_name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
