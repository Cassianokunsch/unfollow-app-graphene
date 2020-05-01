from graphene import ObjectType, String, Int


class Picture(ObjectType):
    pk = String()
    comment_count = Int()
    like_count = Int()
    url = String()
