from InstagramAPI import InstagramAPI
from graphql import GraphQLError
from storage import session
from storage import challenge
from shared.messages import LOGIN_SUCCESS, INVALID_CREDENTIALS_ERROR, CHALLENGE_REQUIRED, UNKNOW_ERROR, CODE_ERROR, LOGOUT_SUCCESS
from shared.constants import BASE_URL
from shared.utils import get_token
from resolvers.types.auth_payload import AuthPayload
import json


def login(username, password):
    api = InstagramAPI(username, password)
    if api.login():
        session.set_session(api.username_id, api)
        return AuthPayload(message=LOGIN_SUCCESS, token=get_token({'id': api.username_id}))
    elif 'invalid_credentials' in list(api.LastJson.keys()):
        raise GraphQLError(INVALID_CREDENTIALS_ERROR)
    elif 'message' in list(api.LastJson.keys()):
        if api.LastJson['message'] == 'challenge_required':
            link = api.LastJson['challenge']['api_path']
            request_code_challenge_api(api, link)
            challenge.set_challenge(api, link)
            return AuthPayload(message=CHALLENGE_REQUIRED, token=get_token({'link': link}))
        else:
            print(api.LastJson)
    else:
        raise GraphQLError(UNKNOW_ERROR)


def send_code_challenge(link, code):
    api = challenge.get_challenge(link)
    code_text = send_code_challenge_api(api, link, code)
    code_json = json.loads(code_text)
    if code_json.get('status') == 'ok':
        if api.login():
            challenge.remove_challenge(link)
            session.set_session(api.username_id, api)
            return AuthPayload(message=LOGIN_SUCCESS, token=get_token({'id': api.username_id}))
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
    session.remove_session(current_pk)
    return LOGOUT_SUCCESS


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
