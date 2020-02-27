from graphene import Mutation, String, ObjectType, Field, NonNull
from instagramApi import login, unfollow, follow, logout, get_user_info, send_code_challenge
from utils import get_current_user, decode_token, get_link_challenge
from typess import AuthPayload


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


class Unfollow(Mutation):

    message = NonNull(String)

    class Arguments:
        user_id_to_unfollow = String(required=True)

    def mutate(root, info, user_id_to_unfollow):
        user = get_current_user(info.context)
        message = unfollow(user, int(user_id_to_unfollow))
        return Unfollow(message=message)


class Follow(Mutation):

    message = NonNull(String)

    class Arguments:
        user_id_to_follow = String(required=True)

    def mutate(root, info, user_id_to_follow):
        user = get_current_user(info.context)
        message = follow(user, int(user_id_to_follow))
        return Follow(message=message)


class SendCodeToChallenge(Mutation):

    Output = AuthPayload

    class Arguments:
        code = String(required=True)

    def mutate(roo, info, code):
        link = get_link_challenge(info.context)
        message, token = send_code_challenge(link, code)
        return AuthPayload(token=token, message=message)


class Mutation(ObjectType):
    login = Login.Field()
    logout = Logout.Field()
    unfollow = Unfollow.Field()
    follow = Follow.Field()
    send_code_challenge = SendCodeToChallenge.Field()
