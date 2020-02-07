from InstagramAPI import InstagramAPI
from graphql import GraphQLError
from constants import INVALID_CREDENTIALS, UNKNOW_ERROR, LOGOUT_ERROR, UNFOLLOW_ERROR, FOLLOW_ERROR
from session import set_user_session, remove_user_session, get_user_session


def login(username, password):
    api = InstagramAPI(username, password)
    if api.login():
        set_user_session(api.username_id, api)
        return api.username_id
    elif api.LastJson['invalid_credentials']:
        raise GraphQLError(INVALID_CREDENTIALS)

    raise GraphQLError(UNKNOW_ERROR)


def logout(username_id):
    api = get_user_session(username_id)
    if api.SendRequest('accounts/logout/'):
        remove_user_session(username_id)
        return "Deslogado com sucesso!"
    raise GraphQLError(LOGOUT_ERROR)


def get_total_followers(username_id):
    api = get_user_session(username_id)
    return api.getTotalFollowers(username_id)


def get_total_followings(username_id):
    api = get_user_session(username_id)
    return api.getTotalFollowings(username_id)


def get_not_followers(username_id):
    lst_not_followers = []
    lst_followers = []
    lst_following = []

    api = get_user_session(username_id)

    lst_following = api.getTotalFollowings(username_id)

    response = api.getTotalFollowers(username_id)

    if len(lst_followers) != len(lst_following):
        for user in response:
            lst_followers.append(user['pk'])

        for following in lst_following:
            if following['pk'] not in lst_followers:
                lst_not_followers.append(following)

    return lst_not_followers


def unfollow(username_id, username_id_to_unfollow):
    api = get_user_session(username_id)
    if api.unfollow(username_id_to_unfollow):
        return "Você parou de seguir!"

    raise GraphQLError(UNFOLLOW_ERROR)


def follow(username_id, username_id_to_follow):
    api = get_user_session(username_id)
    if api.follow(username_id_to_follow):
        return "Você começou a seguir!"

    raise GraphQLError(FOLLOW_ERROR)


def get_user_info(username_id):
    api = get_user_session(username_id)
    if api.getSelfUsernameInfo():
        return api.LastJson['user']

    raise GraphQLError(UNKNOW_ERROR)


def get_user_followers_or_followings(type_user, username_id, max_id):
    api = get_user_session(username_id)

    if type_user == 'followers':
        ok = api.getUserFollowers(username_id, max_id)
    else:
        ok = api.getUserFollowings(username_id, max_id)

    if ok:
        users = api.LastJson['users']
        next_max_id = api.LastJson['next_max_id']
        return users, next_max_id

    raise GraphQLError(UNKNOW_ERROR)
