
from graphene import ObjectType, String,  NonNull


class AuthPayload(ObjectType):
    message = NonNull(String)
    token = NonNull(String)
