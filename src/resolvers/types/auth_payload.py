
from graphene import ObjectType, String,  NonNull


class AuthPayload(ObjectType):
    message = String()
    token = String()
