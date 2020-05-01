from graphene import ObjectType
from resolvers.types.user_interface import UserInterface


class Follower(ObjectType):
    class Meta:
        interfaces = (UserInterface, )
