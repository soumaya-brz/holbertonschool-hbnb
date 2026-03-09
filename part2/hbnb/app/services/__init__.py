from app.repositories.user_repo import UserRepository
from app.repositories.place_repo import PlaceRepository
from app.repositories.amenity_repo import AmenityRepository
from app.services.facade import HBnBFacade

user_repo = UserRepository()
place_repo = PlaceRepository()
amenity_repo = AmenityRepository()

facade_instance = HBnBFacade(user_repo=user_repo, place_repo=place_repo, amenity_repo=amenity_repo)
