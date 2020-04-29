from graphene import ObjectType
from src.resolvers.queries.friends import FriendsQuery
from src.resolvers.queries.user import UserQuery


class Query(FriendsQuery, UserQuery, ObjectType):
    pass
