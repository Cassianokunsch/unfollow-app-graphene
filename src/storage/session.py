from graphql import GraphQLError
from shared.messages import UNAUTHORIZED_ERROR

users_session = dict()


def get_session(username_id):
    try:
        return users_session[username_id]
    except KeyError:
        raise GraphQLError(UNAUTHORIZED_ERROR)


def set_session(username_id, session):
    users_session[username_id] = session


def remove_session(username_id):
    try:
        del users_session[username_id]
    except KeyError:
        raise GraphQLError(UNAUTHORIZED_ERROR)
