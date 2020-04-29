from graphene import Schema
from src.resolvers.queries.query import Query
from src.resolvers.mutations import Mutation

schema = Schema(query=Query, mutation=Mutation)
