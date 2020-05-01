from graphene import ObjectType, String, Int, List
from resolvers.types.unfollower import Unfollower


class MyUnfollowers(ObjectType):
    next_page = String()
    size = Int()
    unfollowers = List(Unfollower)
