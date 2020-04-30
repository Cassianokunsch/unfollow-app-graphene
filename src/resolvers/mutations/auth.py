from graphene import Mutation, String, NonNull
from service.instagramApi import login, logout, send_code_challenge
from shared.utils import get_current_user, get_link_challenge
from resolvers.types.types import AuthPayload


class Login(Mutation):

    Output = AuthPayload

    class Arguments:
        username = String(required=True)
        password = String(required=True)

    def mutate(root, info, username, password):
        message, token = login(username, password)
        return AuthPayload(token=token, message=message)


class Logout(Mutation):

    message = NonNull(String)

    def mutate(root, info):
        user = get_current_user(info.context)
        message = logout(user)
        return Logout(message=message)


class SendCodeToChallenge(Mutation):

    Output = AuthPayload

    class Arguments:
        code = String(required=True)

    def mutate(roo, info, code):
        link = get_link_challenge(info.context)
        message, token = send_code_challenge(link, code)
        return AuthPayload(token=token, message=message)
