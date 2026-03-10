from flask_restx import Namespace, Resource, fields
from app.services import facade_instance as facade

ns = Namespace("places", description="Place operations")

place_model = ns.model("Place", {
    "title": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True)
})


@ns.route("/")
class PlacesRoot(Resource):

    @ns.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200


    @ns.expect(place_model, validate=True)
    @ns.response(201, "Place successfully created")
    @ns.response(400, "Invalid input data")
    def post(self):
        """Create a place"""
        data = ns.payload

        if data.get("price") is None or data["price"] <= 0:
            return {"error": "Price must be positive"}, 400

        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400
