from graphene import Mutation, String, ObjectType, Field
from api.instagram import login, unfollow
from utils import get_current_user
from graphql import GraphQLError
from jwt import encode
from utils import INVALID_CREDENTIALS, UNKNOW, SECRET


class Login(Mutation):
    token = String()

    class Arguments:
        username = String()
        password = String()

    def mutate(root, info, username, password):
        username_id = login(username, password)
        if username_id != INVALID_CREDENTIALS:
            token = encode({'id': username_id}, SECRET,
                           algorithm='HS256').decode('utf-8')
            return Login(token=token)
        else:
            raise GraphQLError("Usuário ou senha inválidos")


class Unfollow(Mutation):
    message = String()

    class Arguments:
        user_id_to_unfollow = String()

    def mutate(root, info, user_id_to_unfollow):
        user = get_current_user(info.context)
        return unfollow(user, user_id_to_unfollow)


class Mutation(ObjectType):
    login = Login.Field()
