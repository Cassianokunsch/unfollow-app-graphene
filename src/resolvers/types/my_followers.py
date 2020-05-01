from graphene import ObjectType, String, Int, List
from resolvers.types.follower import Follower


class MyFollowers(ObjectType):
    next_page = String()
    size = Int()
    followers = List(Follower)
