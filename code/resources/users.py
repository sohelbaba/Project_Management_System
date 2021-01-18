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

        if data['username'] == data['password']:
            return {
                "UsernameSameAsPasswordError": {
                    "meesage": "Username and Password Should be different",
                    "status": 400
                }
            }

        user = UserModel(data['name'], data['username'], data['password'])
        user.save_to_db()
        return jsonify({"Message": "Registration Done..", "status": 200})


class UserLogin(Resource):
    def get(self):
        data = _user_parse.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            if user.status:
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
            return {"message": "User Deactivated. Can't login Again"}
        return {
            "UnauthorizedError": {
                "message": "Invalid username",
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
        # UserModel.query.delete()
        return {"TotalUsers": len(users), "Users": users, "status": 200}


class UserDeactivated(Resource):
    def put(self, id):
        user = UserModel.find_by_id(id)
        if user:
            user.status = False
            user.save_to_db()
            return {"message": "User Deactivated"}
        return {"UserNotExistsError": {
            "meesage": "user with given id doen't Exists",
            "value": 401
        }}
