# app/api/v1/review.py
from flask_restx import Namespace, Resource, fields
from app.services import facade_instance as facade

ns = Namespace("reviews", description="Review operations")

review_model = ns.model("Review", {
    "text": fields.String(required=True),
    "rating": fields.Integer(required=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True)
})

@ns.route("/")
class ReviewsRoot(Resource):
    def get(self):
        """Lister toutes les reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

    def post(self):
        """Créer une nouvelle review"""
        data = ns.payload
        try:
            review = facade.create_review(data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return review.to_dict(), 201
