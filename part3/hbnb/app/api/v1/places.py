from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade_instance as facade

ns = Namespace("places", description="Place operations")

place_model = ns.model(
    "Place",
    {
        "title": fields.String(required=True),
        "description": fields.String(required=False),
        "price": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        "amenities": fields.List(fields.String),
    },
)


@ns.route("/")
class PlaceList(Resource):
    def get(self):
        """List all places (public)"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

    @ns.expect(place_model)
    @jwt_required()
    def post(self):
        """Create a new place (authenticated users only)"""
        current_user_id = get_jwt_identity()
        data = ns.payload
        data["owner_id"] = current_user_id

        try:
            place = facade.create_place(data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return place.to_dict(), 201


@ns.route("/<place_id>")
class PlaceResource(Resource):
    def get(self, place_id):
        """Get place by ID (public)"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @ns.expect(place_model)
    @jwt_required()
    def put(self, place_id):
        """Update place (owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner.id != current_user_id and not claims.get("is_admin"):
            return {"error": "Access forbidden"}, 403

        updated_place = facade.update_place(place_id, ns.payload)
        return updated_place.to_dict(), 200