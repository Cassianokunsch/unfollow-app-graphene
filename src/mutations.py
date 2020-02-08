from graphene import Mutation, String, ObjectType, Field, Boolean
from instagramApi import login, unfollow, follow, logout
from utils import get_current_user
from typess import Payload


class Login(Mutation):

    Output = Payload

    class Arguments:
        username = String(required=True)
        password = String(required=True)

    def mutate(root, info, username, password):
        message, token = login(username, password)
        return Payload(token=token, message=message)


class Logout(Mutation):

    message = NonNull(String)

    def mutate(root, info):
        user = get_current_user(info.context)
        message = logout(user['id'])
        return Logout(message=message)


class Unfollow(Mutation):

    message = NonNull(String)

    class Arguments:
        user_id_to_unfollow = String(required=True)

    def mutate(root, info, user_id_to_unfollow):
        user = get_current_user(info.context)
        message = unfollow(user['id'], int(user_id_to_unfollow))
        return Unfollow(message=message)


class Follow(Mutation):

    message = NonNull(String)

    class Arguments:
        user_id_to_follow = String(required=True)

    def mutate(root, info, user_id_to_follow):
        user = get_current_user(info.context)
        message = follow(user['id'], int(user_id_to_follow))
        return Follow(message=message)


class Mutation(ObjectType):
    login = Login.Field()
    logout = Logout.Field()
    unfollow = Unfollow.Field()
    follow = Follow.Field()
