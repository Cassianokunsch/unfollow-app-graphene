from graphene import ObjectType
from resolvers.mutations.auth import Login, Logout, SendCodeToChallenge
from resolvers.mutations.user import Unfollow, Follow


class Mutation(ObjectType):
    login = Login.Field()
    logout = Logout.Field()
    unfollow = Unfollow.Field()
    follow = Follow.Field()
    send_code_challenge = SendCodeToChallenge.Field()
