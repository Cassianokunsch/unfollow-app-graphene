from graphene import ObjectType
from resolvers.queries.user import UserQuery


class Query(UserQuery, ObjectType):
    pass
