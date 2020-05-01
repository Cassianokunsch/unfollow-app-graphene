from graphene import ObjectType, String, Int, List
from resolvers.types.picture import Picture


class Feed(ObjectType):
    next_page = String()
    size = Int()
    pictures = List(Picture)
