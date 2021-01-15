from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

_user_parse = reqparse.RequestParser()
_user_parse.add_argument('name',
                         type=str,
                         required=False,
                         help='Name is required')
_user_parse.add_argument('username',
                         type=str,
                         required=True,
                         help="Username is required")
_user_parse.add_argument('password',
                         type=str,
                         required=True,
                         help="Password is required")


class User(Resource):
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return jsonify({"user": user})

        return jsonify({"Message": "404 User NotFound."})


class UserRegister(Resource):
    def post(self):
        data = _user_parse.parse_args()
        #check username already exits
        user = UserModel.find_by_username(data['username'])
        if user:
            return jsonify(
                {"Message": "User with this Username already exists.."})

        user = UserModel(data['name'], data['username'], data['password'])
        user.save_to_db()
        return jsonify({"Message": "Registration Done.."})


class UserLogin(Resource):
    def get(self):
        data = _user_parse.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        return jsonify({"Message": "Username or password InCorrect."})


class UserList(Resource):
    def get(self):
        users = [user.json() for user in UserModel.query.all()]
        return jsonify({"Users" : users})