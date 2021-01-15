from config import db


class PermissionModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def json(self):
        return {
            "name": self.name,
            "description": self.description
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.sessoin.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return PermissionModel.query.filter_by(id=id).first()
