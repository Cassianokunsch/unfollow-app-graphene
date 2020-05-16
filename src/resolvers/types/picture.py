from graphene import ObjectType, String, Int, NonNull


class Picture(ObjectType):
    pk = NonNull(String)
    comment_count = NonNull(Int)
    like_count = NonNull(Int)
    url = NonNull(String)
