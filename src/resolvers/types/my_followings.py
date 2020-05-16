from graphene import ObjectType, String, Int, List, NonNull
from resolvers.types.following import Following


class MyFollowings(ObjectType):
    next_page = String()
    size = NonNull(Int)
    followings = NonNull(List(NonNull(Following)))
