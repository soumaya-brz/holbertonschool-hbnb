from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade_instance as facade

ns = Namespace("reviews", description="Review operations")

review_model = ns.model("Review", {
    "text": fields.String(required=True),
    "rating": fields.Integer(required=True),
    "place_id": fields.String(required=True)
})


@ns.route("/")
class ReviewsRoot(Resource):
    @ns.marshal_list_with(review_model)
    def get(self):
        """Lister toutes les reviews (public)"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

    @ns.expect(review_model)
    @ns.marshal_with(review_model, code=201)
    @jwt_required()
    def post(self):
        """Créer une nouvelle review (authenticated users only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        data = ns.payload
        data["user_id"] = current_user_id

        place = facade.get_place(data["place_id"])
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner.id == current_user_id:
            return {"error": "Cannot review your own place"}, 403

        existing_reviews = facade.get_reviews_by_place(place.id)
        for r in existing_reviews:
            if r.user.id == current_user_id:
                return {"error": "You have already reviewed this place"}, 400

        new_review = facade.create_review(data)
        return new_review.to_dict(), 201


@ns.route("/<review_id>")
class ReviewResource(Resource):
    @ns.marshal_with(review_model)
    def get(self, review_id):
        """Get review by ID (public)"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @ns.expect(review_model)
    @ns.marshal_with(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update review (author or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if review.user.id != current_user_id and not claims.get("is_admin"):
            return {"error": "Access forbidden"}, 403

        updated_review = facade.update_review(review_id, ns.payload)
        return updated_review.to_dict(), 200
