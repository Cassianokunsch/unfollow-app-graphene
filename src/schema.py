from graphene import Schema
from resolvers.queries.query import Query
from resolvers.mutations.mutation import Mutation

schema = Schema(query=Query, mutation=Mutation)
