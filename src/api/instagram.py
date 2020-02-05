from InstagramAPI import InstagramAPI
from utils import INVALID_CREDENTIALS, UNKNOW

dic_users_logged = dict()


def login(username, password):
    api = InstagramAPI(username, password)
    if api.login():
        dic_users_logged[api.username_id] = api
        print(dic_users_logged)
        return api.username_id
    elif api.LastJson['invalid_credentials']:
        return INVALID_CREDENTIALS

    return UNKNOW


def get_total_followers(username_id):
    api = dic_users_logged[username_id]
    return api.getTotalFollowers(username_id)


def get_total_followings(username_id):
    api = dic_users_logged[username_id]
    return api.getTotalFollowings(username_id)


def get_not_followers(username_id):
    lst_not_followers = []
    lst_followers = []
    lst_following = []
    api = dic_users_logged[username_id]

    lst_following = api.getTotalFollowings(username_id)

    response = api.getTotalFollowers(username_id)
    for user in response:
        lst_followers.append(user['pk'])

    for following in lst_following:
        if following['pk'] not in lst_followers:
            lst_not_followers.append(following)

    return lst_not_followers


def unfollow(username_id, username_id_to_unfollow):
    api = dic_users_logged[username_id]
    ok = api.unfollow(username_id_to_unfollow)
    print(api.LastJson)
    print(api.LastResponse)
    if ok:
        return "Você parou de seguir " + username_id_to_unfollow
    else:
        return "Ocorreu um erro ao tentar para de seguir " + username_id_to_unfollow
