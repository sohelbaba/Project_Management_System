from config import db


class UserModel(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Boolean, default=True)

    projects = db.relationship('ProjectModel', backref='user')

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def json(self):
        # json represantation of model object
        return {
            "name": self.name,
            "username": self.username,
            "password": hash(self.password)
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return UserModel.query.filter_by(id=id).first()
