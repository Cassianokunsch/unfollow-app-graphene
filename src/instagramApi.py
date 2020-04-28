from InstagramAPI import InstagramAPI
from graphql import GraphQLError
from jwt import encode
from constants import INVALID_CREDENTIALS_ERROR, UNKNOW_ERROR, LOGOUT_ERROR, TOO_MANY_REQUESTS, UNFOLLOW_ERROR, FOLLOW_ERROR, SEND_CODE, LOGIN_SUCCESS, CHALLENGE_REQUIRED, BASE_URL, CODE_ERROR, LOGOUT_SUCCESS, FOLLOW_SUCCESS, UNFOLLOW_SUCCESS
from auth import set_user_session, remove_user_session, get_user_session, set_user_challenge, get_user_challenge, remove_user_challenge
from utils import get_token
from typess import PictureType
import time
import os
import json


class User:

    def __init__(self, api):
        super().__init__()
        self.api = api
        self.lst_followers = []
        self.lst_followings = []
        self.lst_unfollowers = self.get_unfollowers()

    def get_unfollowers(self):
        lst_pks = []
        lst_unfollowers = []

        try:
            self.lst_followings = self.api.getTotalFollowings(
                self.api.username_id)
            self.lst_followers = self.api.getTotalFollowers(
                self.api.username_id)
        except Exception:
            pass

        if self.api.LastJson['status'] == 'fail':
            if self.api.LastJson['message'] == 'Please wait a few minutes before you try again.':
                raise GraphQLError(TOO_MANY_REQUESTS)

            print(self.api.LastJson['message'])
            raise GraphQLError(UNKNOW_ERROR)

        for user in self.lst_followers:
            lst_pks.append(user['pk'])

        for following in self.lst_followings:
            if following['pk'] not in lst_pks:
                lst_unfollowers.append(following)

        return lst_unfollowers

    def get_me(self):
        if self.api.getUsernameInfo(self.api.username_id):
            return self.api.LastJson['user']

        raise GraphQLError(UNKNOW_ERROR)

    def get_followers(self,  next_page):
        if self.api.getUserFollowers(self.api.username_id, next_page):
            users = self.api.LastJson['users']
            next_page = self.api.LastJson['next_max_id']
            self.lst_followers = users
            return users, next_page
        else:
            response = self.api.LastJson
            if response['message'] == 'Please wait a few minutes before you try again.':
                raise GraphQLError(TOO_MANY_REQUESTS)

        raise GraphQLError(UNKNOW_ERROR)

    def get_followings(self,  next_page):
        if self.api.getUserFollowings(self.api.username_id, next_page):
            users = self.api.LastJson['users']
            next_page = self.api.LastJson['next_max_id']
            self.lst_followings = users
            return users, next_page
        else:
            response = self.api.LastJson
            if response['message'] == 'Please wait a few minutes before you try again.':
                raise GraphQLError(TOO_MANY_REQUESTS)

        raise GraphQLError(UNKNOW_ERROR)

    def get_user_feed(self, username_id, next_page):
        if self.api.getUserFeed(username_id, next_page):
            response = self.api.LastJson['items']

            lst = []

            for item in response:
                if "carousel_media" in list(item.keys()):
                    url = item["carousel_media"][0]["image_versions2"]["candidates"][0]["url"]
                else:
                    url = item["image_versions2"]["candidates"][0]["url"]

                lst.append(
                    PictureType(
                        pk=item['pk'],
                        comment_count=item['comment_count'],
                        like_count=item['like_count'],
                        url=url
                    ))

            return lst, item["next_max_id"]

        raise GraphQLError(UNKNOW_ERROR)


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
        c = User(api)
        set_user_session(api.username_id, c)
        print(c)
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
            set_user_session(api.username_id, User(api))
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


def logout(current_pk):
    remove_user_session(current_pk)
    return LOGOUT_SUCCESS


def get_not_followers(current_pk):
    lst_not_followers = []
    lst_followers = []
    lst_following = []

    api = get_user_session(current_pk)

    try:
        lst_following = api.getTotalFollowings(current_pk)
        response = api.getTotalFollowers(current_pk)
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


def unfollow(current_pk, pk):
    api = get_user_session(current_pk)
    if api.unfollow(pk):
        return UNFOLLOW_SUCCESS

    raise GraphQLError(UNFOLLOW_ERROR)


def follow(current_pk, pk):
    api = get_user_session(current_pk)
    if api.follow(pk):
        return FOLLOW_SUCCESS

    raise GraphQLError(FOLLOW_ERROR)


def get_user_info(current_pk, pk):
    api = get_user_session(current_pk)
    if api.getUsernameInfo(pk):
        return api.LastJson['user']

    raise GraphQLError(UNKNOW_ERROR)


def get_me(current_pk):
    api = get_user_session(current_pk)
    if api.getUsernameInfo(current_pk):
        return api.LastJson['user']

    raise GraphQLError(UNKNOW_ERROR)


def get_user_followers_or_followings(type_user, current_pk, max_id):
    api = get_user_session(current_pk)

    if type_user == 'followers':
        ok = api.getUserFollowers(current_pk, max_id)
    else:
        ok = api.getUserFollowings(current_pk, max_id)

    if ok:
        users = api.LastJson['users']
        next_max_id = api.LastJson['next_max_id']
        return users, next_max_id
    else:
        response = api.LastJson
        if response['message'] == 'Please wait a few minutes before you try again.':
            raise GraphQLError(TOO_MANY_REQUESTS)

    raise GraphQLError(UNKNOW_ERROR)
