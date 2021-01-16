from config import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text, DateTime
from models.permission import PermissionModel
import datetime
import re
import uuid
import base64


def UUID_URI64():
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {
        '+': '-',
        '/': '_',
        '=': ''
    }[m.group(0)], rv)


class ProjectModel(db.Model):

    __tablename__ = 'project'

    uuid = db.Column(db.Text(length=36),
                     default=lambda: str(UUID_URI64()),
                     primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('UserModel',
                                 foreign_keys="ProjectModel.created_by_id")
    project_color_identity = db.Column(db.String(20), unique=True)
    created_at = db.Column(DateTime, default=datetime.datetime.now)

    collaborators = db.relationship(
        'ShareProjectModel', cascade="all,delete", backref='project')

    tasks = db.relationship(
        'TaskModel', cascade="all,delete", backref='project')

    def __init__(self, name, description, created_by_id, project_color_identity):
        self.name = name
        self.description = description
        self.created_by_id = created_by_id
        self.project_color_identity = project_color_identity

    def json(self):

        return {
            "UUID": self.uuid,
            "Project_Name": self.name,
            "Project_Description": self.description,
            "Created_by": self.created_by.id,
            "Created_at": str(self.created_at),
            "Project_color_identity": self.project_color_identity,
            "Collaborators": [user.json() for user in self.collaborators],
            "Tasks": [task.json() for task in self.tasks]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return ProjectModel.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return ProjectModel.query.filter_by(uuid=id).first()
