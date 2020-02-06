from jwt import decode
from graphql import GraphQLError


INVALID_CREDENTIALS = "Usuário ou senha inválidos!"
UNAUTHORIZED = "Não autorizado. Você precisa estar logado!"
TOKEN_ERROR = 'Essa requisição precisa do token JWT'
UNKNOW_ERROR = "Erro desconhecido"
SECRET = 'secret'
LOGOUT_ERROR = "Ocorreu um erro ao tentar deslogar!"
UNFOLLOW_ERROR = "Ocorreu um problema na hora de parar de seguir o usuário!"
FOLLOW_ERROR = "Ocorreu um problema na hora de seguir o usuário!"


def get_current_user(context):
    token = context.headers.get("Authorization")
    if not token:
        raise GraphQLError(TOKEN_ERROR)

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
