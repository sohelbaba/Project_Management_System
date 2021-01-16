from flask import Flask
from flask_restful import Api
from resources.users import UserLogin, UserRegister, UserList, UserLogout
from resources.projects import Project, ProjectList, AllProjectsList
from resources.shareproject import ProjectShare
from resources.task import Task, TaskList
from resources.permission import Permission
from flask_jwt_extended import JWTManager

app = Flask(__name__)  # flask object
app.secret_key = 'PROJECT_MANAGMENT_SECRET_KEY'
jwt = JWTManager(app)

api = Api(app)  # api instance
# set database url
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

blacklist = set()

# before first request create database


@app.before_first_request
def init():
    db.create_all()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@jwt.expired_token_loader
def token_expired():
    return {
        "UnauthorizedError": {
            "message": "Login Required",
            "status": 401
        }
    }


@jwt.invalid_token_loader
def invalid_toke(error):
    return {
        "UnauthorizedError": {
            "message": "Access Token Invalid",
            "status": 401
        }
    }


@jwt.unauthorized_loader
def unauthorized(error):
    return {
        "UnauthorizedError": {
            "message": "Login Required",
            "status": 401
        }
    }


# endpoints
api.add_resource(UserRegister, '/registration')
api.add_resource(UserLogin, '/authentication')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserList, '/users')
api.add_resource(Project, '/project/<string:name>')
api.add_resource(ProjectShare, '/project/share')
api.add_resource(ProjectList, '/projects')
api.add_resource(AllProjectsList, '/Allprojects')
api.add_resource(Task, '/project/task/<string:name>')
api.add_resource(TaskList, '/project/task')
api.add_resource(Permission, '/permission')

if __name__ == '__main__':
    from config import db
    db.init_app(app)
    app.run(port=5000, debug=True)
