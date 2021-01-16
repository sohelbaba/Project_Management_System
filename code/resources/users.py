from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_raw_jwt, jwt_required
from validations import non_empty_string

blacklist = set()

_user_parse = reqparse.RequestParser()
_user_parse.add_argument('name',
                         type=non_empty_string,
                         required=False,
                         help='Name is required')
_user_parse.add_argument('username',
                         type=non_empty_string,
                         required=True,
                         help="Username is required")
_user_parse.add_argument('password',
                         type=non_empty_string,
                         required=True,
                         help="Password is required")


class User(Resource):
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return user.json()

        return {
            "UserNotExistsError": {
                "message": "User with given username doesn't exists",
                "status": 400
            }}


class UserRegister(Resource):
    def post(self):
        data = _user_parse.parse_args()

        # check username already exits
        user = UserModel.find_by_username(data['username'])
        if user:
            return jsonify(
                {"UserNameAlreadyExistsError": {
                    "message": "User with given name already exists",
                    "status": 400
                }})

        user = UserModel(data['name'], data['username'], data['password'])
        user.save_to_db()
        return jsonify({"Message": "Registration Done..", "status": 200})


class UserLogin(Resource):
    def get(self):
        data = _user_parse.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return {
                "access_token": access_token,
                "status": 200
            }

        return {
            "UnauthorizedError": {
                "message": "Invalid username or password",
                "status": 401
            }}


class UserLogout(Resource):

    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"message": "Successfully logged out"}


class UserList(Resource):
    def get(self):
        users = [user.json() for user in UserModel.query.all()]
        return {"Users": users, "status": 200}
