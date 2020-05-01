from jwt import decode, encode
from graphql import GraphQLError
from shared.vars import SECRET, ALGORITHM
from shared.messages import CHALLENGE_REQUIRED, INVALID_TOKEN, TOKEN_ERROR


def get_token(data):
    return encode(data, SECRET, algorithm=ALGORITHM).decode('utf-8')


def decode_token(token):
    return decode(token, SECRET, algorithm=ALGORITHM)


def get_current_user(context):
    authorization = context.headers.get("Authorization")
    if(authorization != None):
        token = authorization.replace('Bearer ', '')
        if token != "":
            data = decode_token(token)
            if 'id' in list(data.keys()):
                return decode_token(token)['id']
            elif 'link' in list(data.keys()):
                raise GraphQLError(CHALLENGE_REQUIRED)
            else:
                raise GraphQLError(INVALID_TOKEN)

    raise GraphQLError(TOKEN_ERROR)


def get_link_challenge(context):
    authorization = context.headers.get("Authorization")
    if(authorization != None):
        token = authorization.replace('Bearer ', '')
        if token != "":
            data = decode_token(token)
            if 'link' in list(data.keys()):
                return decode_token(token)['link']
            else:
                raise GraphQLError(INVALID_TOKEN)

    raise GraphQLError(TOKEN_ERROR)


def parser_fields_int_to_string(data):
    for user in data:
        keys = user.keys()
        for key in keys:
            value = (user[key])
            if isinstance(value, int) and not isinstance(value, bool):
                user[key] = str(value)

    return data
