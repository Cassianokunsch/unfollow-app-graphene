from graphene import ObjectType, String, Int, List
from resolvers.types.following import Following


class MyFollowings(ObjectType):
    next_page = String()
    size = Int()
    followings = List(Following)
