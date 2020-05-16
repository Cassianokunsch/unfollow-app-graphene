from graphene import ObjectType, String, Int, List, NonNull
from resolvers.types.follower import Follower


class MyFollowers(ObjectType):
    next_page = String()
    size = NonNull(Int)
    followers = NonNull(List(NonNull(Follower)))
