from graphene import ObjectType, String, Int, List, NonNull
from resolvers.types.picture import Picture


class Feed(ObjectType):
    next_page = String()
    size = NonNull(Int)
    pictures = NonNull(List(NonNull(Picture)))
