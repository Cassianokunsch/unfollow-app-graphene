from graphene import Mutation, String, NonNull
from service.auth import login, logout, send_code_challenge
from shared.utils import get_current_user, get_link_challenge
from resolvers.types.auth_payload import AuthPayload


class Login(Mutation):

    Output = NonNull(AuthPayload)

    class Arguments:
        username = String(required=True)
        password = String(required=True)

    def mutate(root, info, username, password):
        return login(username, password)


class Logout(Mutation):

    message = NonNull(String)

    def mutate(root, info):
        user = get_current_user(info.context)
        message = logout(user)
        return Logout(message=message)


class SendCodeToChallenge(Mutation):

    Output = NonNull(AuthPayload)

    class Arguments:
        code = String(required=True)

    def mutate(roo, info, code):
        link = get_link_challenge(info.context)
        return send_code_challenge(link, code)
