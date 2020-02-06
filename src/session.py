from graphql import GraphQLError
from utils import UNAUTHORIZED

users_session = dict()


def get_user_session(username_id):
    try:
        return users_session[username_id]
    except KeyError:
        raise GraphQLError(UNAUTHORIZED)


def set_user_session(username_id, session):
    try:
        users_session[username_id] = session
    except KeyError:
        raise GraphQLError(UNAUTHORIZED)


def remove_user_session(username_id):
    try:
        del users_session[username_id]
    except KeyError:
        raise GraphQLError(UNAUTHORIZED)
