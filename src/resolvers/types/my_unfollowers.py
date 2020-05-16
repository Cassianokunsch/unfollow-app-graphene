from graphene import ObjectType, String, Int, List, NonNull
from resolvers.types.unfollower import Unfollower


class MyUnfollowers(ObjectType):
    next_page = NonNull(String)
    size = NonNull(Int)
    unfollowers = NonNull(List(NonNull(Unfollower)))
