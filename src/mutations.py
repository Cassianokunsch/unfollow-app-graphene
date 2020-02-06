from graphene import Mutation, String, ObjectType, Field, Int, Boolean
from api.instagram import login, unfollow
from utils import get_current_user
from jwt import encode
from utils import SECRET
MutationResponseInterface


class MutationResponse(Interface):
    code: String()
    success: Boolean()
    message: String()


class UnfollowMutationResponse(ObjectType):
    class Meta:
        interfaces = (MutationResponse, )


class Login(Mutation):
    token = String()

    class Arguments:
        username = String()
        password = String()

    def mutate(root, info, username, password):
        username_id = login(username, password)
        token = encode({'id': username_id}, SECRET,
                       algorithm='HS256').decode('utf-8')
        return Login(token=token)


class Unfollow(Mutation):
    message = String()
    code = String()

    class Arguments:
        user_id_to_unfollow = Int()

    def mutate(root, info, user_id_to_unfollow):
        user = get_current_user(info.context)
        if unfollow(user['id'], user_id_to_unfollow):
            message = "ok"
            code = "200"
        else:
            message = "Error"
            code = "404"
        return message, code


class Follow(Mutation):
    message = String()

    class Arguments:
        user_id_to_follow = Int()

    def mutate(root, info, user_id_to_follow):
        user = get_current_user(info.context)
        return follow(user['id'], user_id_to_follow)


class Mutation(ObjectType):
    login = Login.Field()
    unfollow = Unfollow.Field()
    follow = Follow.Field()
