from jwt import decode
from graphql import GraphQLError


INVALID_CREDENTIALS = "Usuário ou senha inválidos!"
UNAUTHORIZED = "Não autorizado. Você precisa estar logado!"
UNKNOW = "Erro desconhecido"
SECRET = 'secret'


def get_current_user(context):
    token = context.headers.get("Authorization")
    if not token:
        raise GraphQLError(UNAUTHORIZED)

    user = decode(token, SECRET, algorithms=['HS256'])
    return user


def parser_fields_int_to_string(data):
    for user in data:
        keys = user.keys()
        for key in keys:
            value = (user[key])
            if isinstance(value, int) and not isinstance(value, bool):
                user[key] = str(value)

    return data
