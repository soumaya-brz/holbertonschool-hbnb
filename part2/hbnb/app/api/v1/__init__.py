from flask_restx import Api
from .places import ns as places_ns
from .users import ns as users_ns
from .amenities import ns as amenities_ns

api = Api(title="HBNB API", version="1.0")

api.add_namespace(users_ns, path="/api/v1/users")
api.add_namespace(places_ns, path="/api/v1/places")
api.add_namespace(amenities_ns, path="/api/v1/amenities")
