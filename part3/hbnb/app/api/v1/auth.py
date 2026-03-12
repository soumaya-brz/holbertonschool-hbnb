from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade_instance as facade

ns = Namespace("auth", description="Authentication operations")

login_model = ns.model("Login", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
})

@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model, validate=True)
    @ns.response(200, "Login successful")
    @ns.response(401, "Invalid email or password")
    def post(self):
        data = ns.payload
        email = data.get("email")
        password = data.get("password")

        user = facade.get_user_by_email(email)
        if not user or not user.check_password(password):
            return {"error": "Invalid email or password"}, 401

        access_token = create_access_token(identity=user.id, additional_claims={"is_admin": user.is_admin})

        return {"access_token": access_token}, 200