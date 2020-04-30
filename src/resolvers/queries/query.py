from graphene import ObjectType
from resolvers.queries.friends import FriendsQuery
from resolvers.queries.user import UserQuery


class Query(FriendsQuery, UserQuery, ObjectType):
    pass
