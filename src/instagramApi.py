from InstagramAPI import InstagramAPI
from graphql import GraphQLError
from jwt import encode
from constants import INVALID_CREDENTIALS_ERROR, UNKNOW_ERROR, LOGOUT_ERROR, UNFOLLOW_ERROR, FOLLOW_ERROR, SEND_CODE, LOGIN_SUCCESS, CHALLENGE_REQUIRED, BASE_URL, CODE_ERROR, LOGOUT_SUCCESS, FOLLOW_SUCCESS, UNFOLLOW_SUCCESS
from auth import set_user_session, remove_user_session, get_user_session, set_user_challenge, get_user_challenge, remove_user_challenge
from utils import get_token
import time
import os
import json


def request_code_challenge_api(api, checkpoint_url):
    api.s.headers.update({'Referer': BASE_URL})
    req = api.s.get(BASE_URL[:-1] + checkpoint_url)
    api.s.headers.update(
        {'X-CSRFToken': req.cookies['csrftoken'], 'X-Instagram-AJAX': '1'})
    api.s.headers.update({'Referer': BASE_URL[:-1] + checkpoint_url})
    challenge_data = {'choice': 0}
    challenge = api.s.post(
        BASE_URL[:-1] + checkpoint_url, data=challenge_data, allow_redirects=True)
    api.s.headers.update(
        {'X-CSRFToken': challenge.cookies['csrftoken'], 'X-Instagram-AJAX': '1'})


def send_code_challenge_api(api, checkpoint_url, code):
    code_data = {'security_code': code}
    code = api.s.post(BASE_URL[:-1] + checkpoint_url,
                      data=code_data, allow_redirects=True)
    api.s.headers.update({'X-CSRFToken': code.cookies['csrftoken']})
    api.cookies = code.cookies
    return code.text


def login(username, password):
    api = InstagramAPI(username, password)
    if api.login():
        set_user_session(api.username_id, api)
        return LOGIN_SUCCESS, get_token({'id': api.username_id})
    elif 'invalid_credentials' in list(api.LastJson.keys()):
        raise GraphQLError(INVALID_CREDENTIALS_ERROR)
    elif api.LastJson['message'] == 'challenge_required':
        link = api.LastJson['challenge']['api_path']
        request_code_challenge_api(api, link)
        set_user_challenge(api, link)
        return CHALLENGE_REQUIRED, get_token({'link': link})
    else:
        raise GraphQLError(UNKNOW_ERROR)


def send_code_challenge(link, code):
    api = get_user_challenge(link)
    code_text = send_code_challenge_api(api, link, code)
    code_json = json.loads(code_text)
    if code_json.get('status') == 'ok':
        if api.login():
            remove_user_challenge(link)
            set_user_session(api.username_id, api)
            return LOGIN_SUCCESS, get_token({'id': api.username_id})
        else:
            raise GraphQLError(UNKNOW_ERROR)
    elif 'errors' in code_text:
        if code_json.get('challenge').get('errors')[0] == 'Please check the code we sent you and try again.':
            raise GraphQLError(CODE_ERROR)
        else:
            raise GraphQLError(code_json.get('challenge').get('errors')[0])
    else:
        raise GraphQLError(json.dumps(code_text))


def logout(username_id):
    remove_user_session(username_id)
    return LOGOUT_SUCCESS


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

    for user in response:
        lst_followers.append(user['pk'])

    for following in lst_following:
        if following['pk'] not in lst_followers:
            lst_not_followers.append(following)

    return lst_not_followers


def unfollow(username_id, username_id_to_unfollow):
    api = get_user_session(username_id)
    if api.unfollow(username_id_to_unfollow):
        return UNFOLLOW_SUCCESS

    raise GraphQLError(UNFOLLOW_ERROR)


def follow(username_id, username_id_to_follow):
    api = get_user_session(username_id)
    if api.follow(username_id_to_follow):
        return FOLLOW_SUCCESS

    raise GraphQLError(FOLLOW_ERROR)


def get_user_info(username_id):
    api = get_user_session(username_id)
    if api.getUsernameInfo(username_id):
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
