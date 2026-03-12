from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade_instance as facade

ns = Namespace("amenities", description="Amenity operations")

amenity_model = ns.model("Amenity", {
    "name": fields.String(required=True, description="Name of the amenity")
})

@ns.route("/")
class AmenityList(Resource):
    @ns.expect(amenity_model, validate=True)
    @jwt_required()
    def post(self):
        """Register a new amenity (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Access forbidden"}, 403

        data = ns.payload
        amenity = facade.create_amenity(data)
        return {"id": amenity.id, "name": amenity.name}, 201

    @ns.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve a list of all amenities (public)"""
        amenities = facade.get_all_amenities()
        return [{"id": a.id, "name": a.name} for a in amenities], 200


@ns.route("/<amenity_id>")
class AmenityResource(Resource):
    @ns.response(200, "Amenity details retrieved successfully")
    @ns.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get amenity details by ID (public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {"id": amenity.id, "name": amenity.name}, 200

    @ns.expect(amenity_model, validate=True)
    @ns.response(200, "Amenity updated successfully")
    @ns.response(404, "Amenity not found")
    @ns.response(400, "Invalid input data")
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Access forbidden"}, 403

        data = ns.payload
        updated = facade.update_amenity(amenity_id, data)
        if not updated:
            return {"error": "Amenity not found"}, 404
        return {"id": updated.id, "name": updated.name}, 200