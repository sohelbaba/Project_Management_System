from config import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text
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
    share_with_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    created_by = db.relationship('UserModel',
                                 foreign_keys="ProjectModel.created_by_id")

    share_by = db.relationship('UserModel',
                               foreign_keys="ProjectModel.share_with_id")

    permissions = db.Column(db.Integer, default=None)

    tasks = db.relationship('TaskModel', backref='project')

    def __init__(self, name, description, created_by_id):
        self.name = name
        self.description = description
        self.created_by_id = created_by_id

    def json(self):

        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by_id,
            "share_with": self.share_with_id,
            "permission": self.permissions,
            "Tasks": "not yet"
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