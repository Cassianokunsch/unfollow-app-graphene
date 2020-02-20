from InstagramAPI import InstagramAPI
from graphql import GraphQLError
from jwt import encode
from constants import INVALID_CREDENTIALS, UNKNOW_ERROR, LOGOUT_ERROR, UNFOLLOW_ERROR, FOLLOW_ERROR, SECRET, SEND_CODE
from session import set_user_session, remove_user_session, get_user_session
import time
import os
import json


def request_code_challenge(self, checkpoint_url):
    BASE_URL = 'https://www.instagram.com/'
    self.s.headers.update({'Referer': BASE_URL})
    req = self.s.get(BASE_URL[:-1] + checkpoint_url)
    self.s.headers.update(
        {'X-CSRFToken': req.cookies['csrftoken'], 'X-Instagram-AJAX': '1'})
    self.s.headers.update({'Referer': BASE_URL[:-1] + checkpoint_url})
    challenge_data = {'choice': 0}
    challenge = self.s.post(
        BASE_URL[:-1] + checkpoint_url, data=challenge_data, allow_redirects=True)
    self.s.headers.update(
        {'X-CSRFToken': challenge.cookies['csrftoken'], 'X-Instagram-AJAX': '1'})


def send_code_challenge(checkpoint_url, code):
    code_data = {'security_code': code}
    code = self.s.post(BASE_URL[:-1] + checkpoint_url,
                       data=code_data, allow_redirects=True)
    self.s.headers.update({'X-CSRFToken': code.cookies['csrftoken']})
    self.cookies = code.cookies
    code_text = json.loads(code.text)
    if code_text.get('status') == 'ok':
        self.authenticated = True
        self.logged_in = True
    elif 'errors' in code.text:
        for count, error in enumerate(code_text['challenge']['errors']):
            count += 1
            logging.error(
                'Session error %(count)s: "%(error)s"' % locals())
    else:
        logging.error(json.dumps(code_text))


def login(username, password):
    api = InstagramAPI(username, password)
    if api.login():
        set_user_session(api.username_id, api)
        return "Logado com sucesso!", encode({'id': api.username_id}, SECRET,
                                             algorithm='HS256').decode('utf-8')
    elif 'invalid_credentials' in list(api.LastJson.keys()):
        raise GraphQLError(INVALID_CREDENTIALS)
    elif api.LastJson['message'] == 'challenge_required':
        api.request_code_challenge = request_code_challenge
        api.send_code_challenge = send_code_challenge

        link = api.LastJson['challenge']['api_path']
        api.request_code_challenge(link)
        set_user_challenge(api, link)
        GraphQLError(SEND_CODE)
    else:
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
