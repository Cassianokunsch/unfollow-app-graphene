from graphene import ObjectType
from resolvers.types.user_interface import UserInterface


class Unfollower(ObjectType):
    class Meta:
        interfaces = (UserInterface, )
