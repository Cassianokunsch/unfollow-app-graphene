from graphql import GraphQLError
from shared.messages import UNAUTHORIZED_CHALLENGE_ERROR

users_challenge = dict()


def set_challenge(api, link):
    users_challenge[link] = api


def get_challenge(link):
    try:
        return users_challenge[link]
    except KeyError:
        raise GraphQLError(UNAUTHORIZED_CHALLENGE_ERROR)


def remove_challenge(link):
    try:
        del users_challenge[link]
    except KeyError:
        raise GraphQLError(UNAUTHORIZED_CHALLENGE_ERROR)
