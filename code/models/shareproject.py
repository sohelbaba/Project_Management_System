from config import db
from models.user import UserModel


class ShareProjectModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), db.ForeignKey(
        'project.uuid'), default=None)
    share_with_id = db.Column(db.Integer, default=None)
    permission = db.Column(db.Integer, default=None)

    def __init__(self, uuid, share_with_id, permission):
        self.uuid = uuid
        self.share_with_id = share_with_id
        self.permission = permission

    def json(self):
        return {
            "Collaborator": UserModel.find_by_id(self.share_with_id).json()['name'],
            "permission": self.permission,
            "uuid": self.uuid

        }

    @classmethod
    def find_by_id(cls, id):
        return ShareProjectModel.query.filter_by(share_with_id=id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
