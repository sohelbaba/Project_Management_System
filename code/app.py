from flask import Flask
from flask_restful import Api
from resources.users import UserLogin, UserRegister
from resources.projects import Project, ProjectShare, ProjectList
from resources.task import Task, TaskList
from resources.permission import Permission
from models.permission import PermissionModel
from flask_jwt_extended import JWTManager

app = Flask(__name__)  #flask object
app.secret_key = 'PROJECT_MANAGMENT_SECRET_KEY'
jwt = JWTManager(app)

api = Api(app)  # api instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  #set database url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#before first request create database
@app.before_first_request
def init():
    db.create_all()


@jwt.expired_token_loader
def token_expired():
    return {"message": "You Need To login Again.."}, 401


@jwt.invalid_token_loader
def invalid_toke(error):
    return {"message": "Provided token is invalid "}, 401


@jwt.unauthorized_loader
def unauthorized(error):
    return {"message": "Unauthorized entry "}, 401


#endpoints
api.add_resource(UserRegister, '/registration')
api.add_resource(UserLogin, '/authentication')
api.add_resource(Project, '/project/<string:name>')
api.add_resource(ProjectShare, '/project/share')
api.add_resource(ProjectList, '/projects/<int:id>')
api.add_resource(Task, '/project/task/<string:name>')
api.add_resource(TaskList, '/project/task')
api.add_resource(Permission, '/permission')

if __name__ == '__main__':
    from config import db
    db.init_app(app)
    app.run(port=5000, debug=True)
