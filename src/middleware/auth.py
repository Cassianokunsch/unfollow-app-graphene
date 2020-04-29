from graphql import GraphQLError
from src.shared.constants import UNAUTHORIZED_ERROR, UNAUTHORIZED_CHALLENGE_ERROR

users_session = dict()
users_challenge = dict()


def get_user_session(username_id):
    try:
        return users_session[username_id]
    except KeyError:
        raise GraphQLError(UNAUTHORIZED_ERROR)


def set_user_session(username_id, session):
    users_session[username_id] = session


def remove_user_session(username_id):
    try:
        del users_session[username_id]
    except KeyError:
        raise GraphQLError(UNAUTHORIZED_ERROR)


def set_user_challenge(api, link):
    users_challenge[link] = api


def get_user_challenge(link):
    try:
        return users_challenge[link]
    except KeyError:
        raise GraphQLError(UNAUTHORIZED_CHALLENGE_ERROR)


def remove_user_challenge(link):
    try:
        del users_challenge[link]
    except KeyError:
        raise GraphQLError(UNAUTHORIZED_CHALLENGE_ERROR)
