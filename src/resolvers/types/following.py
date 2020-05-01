from graphene import ObjectType
from resolvers.types.user_interface import UserInterface


class Following(ObjectType):
    class Meta:
        interfaces = (UserInterface, )
