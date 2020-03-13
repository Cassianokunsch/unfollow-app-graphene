from InstagramAPI import InstagramAPI
from graphql import GraphQLError
from jwt import encode
from constants import INVALID_CREDENTIALS_ERROR, UNKNOW_ERROR, LOGOUT_ERROR, TOO_MANY_REQUESTS, UNFOLLOW_ERROR, FOLLOW_ERROR, SEND_CODE, LOGIN_SUCCESS, CHALLENGE_REQUIRED, BASE_URL, CODE_ERROR, LOGOUT_SUCCESS, FOLLOW_SUCCESS, UNFOLLOW_SUCCESS
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
    elif 'message' in list(api.LastJson.keys()):
        if api.LastJson['message'] == 'challenge_required':
            link = api.LastJson['challenge']['api_path']
            request_code_challenge_api(api, link)
            set_user_challenge(api, link)
            return CHALLENGE_REQUIRED, get_token({'link': link})
        else:
            print(api.LastJson)
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


def logout(current_user_pk):
    remove_user_session(current_user_pk)
    return LOGOUT_SUCCESS


def get_not_followers(current_user_pk):
    lst_not_followers = []
    lst_followers = []
    lst_following = []

    api = get_user_session(current_user_pk)

    try:
        lst_following = api.getTotalFollowings(current_user_pk)
        response = api.getTotalFollowers(current_user_pk)
    except Exception:
        pass

    if api.LastJson['status'] == 'fail':
        if api.LastJson['message'] == 'Please wait a few minutes before you try again.':
            raise GraphQLError(TOO_MANY_REQUESTS)

        print(api.LastJson['message'])
        raise GraphQLError(UNKNOW_ERROR)

    for user in response:
        lst_followers.append(user['pk'])

    for following in lst_following:
        if following['pk'] not in lst_followers:
            lst_not_followers.append(following)

    return lst_not_followers


def unfollow(current_user_pk, pk):
    api = get_user_session(current_user_pk)
    if api.unfollow(pk):
        return UNFOLLOW_SUCCESS

    raise GraphQLError(UNFOLLOW_ERROR)


def follow(current_user_pk, pk):
    api = get_user_session(current_user_pk)
    if api.follow(pk):
        return FOLLOW_SUCCESS

    raise GraphQLError(FOLLOW_ERROR)


def get_user_info(current_user_pk, pk):
    api = get_user_session(current_user_pk)
    if api.getUsernameInfo(pk):
        return api.LastJson['user']

    raise GraphQLError(UNKNOW_ERROR)


def get_me(current_user_pk):
    api = get_user_session(current_user_pk)
    if api.getUsernameInfo(current_user_pk):
        return api.LastJson['user']

    raise GraphQLError(UNKNOW_ERROR)


def get_user_followers_or_followings(type_user, current_user_pk, max_id):
    api = get_user_session(current_user_pk)

    if type_user == 'followers':
        ok = api.getUserFollowers(current_user_pk, max_id)
    else:
        ok = api.getUserFollowings(current_user_pk, max_id)

    if ok:
        users = api.LastJson['users']
        next_max_id = api.LastJson['next_max_id']
        return users, next_max_id
    else:
        response = api.LastJson
        if response['message'] == 'Please wait a few minutes before you try again.':
            raise GraphQLError(TOO_MANY_REQUESTS)

    raise GraphQLError(UNKNOW_ERROR)
