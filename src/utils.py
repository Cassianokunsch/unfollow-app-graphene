from jwt import decode
from graphql import GraphQLError


INVALID_CREDENTIALS = -1
UNKNOW = -999
SECRET = 'secret'


def get_current_user(context):
    token = context.headers.get("Authorization")
    if not token:
        raise GraphQLError("You must be authenticated!")

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
