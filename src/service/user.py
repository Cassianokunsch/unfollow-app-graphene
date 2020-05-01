from graphql import GraphQLError
from shared.messages import UNKNOW_ERROR, TOO_MANY_REQUESTS, UNFOLLOW_SUCCESS, UNFOLLOW_ERROR, FOLLOW_SUCCESS, FOLLOW_ERROR
from resolvers.types.user_info import UserInfo
from resolvers.types.picture import Picture
from resolvers.types.feed import Feed
from storage.session import get_session

MESSAGE_ERROR = 'Please wait a few minutes before you try again.'


def get_user_info(current_pk, pk):
    api = get_session(current_pk)

    if pk == '':
        ok = api.getUsernameInfo(current_pk)
    else:
        ok = api.getUsernameInfo(pk)

    if ok:
        return UserInfo(pk=api.LastJson['user']['pk'],
                        username=api.LastJson['user']['username'],
                        full_name=api.LastJson['user']['full_name'],
                        is_private=api.LastJson['user']['is_private'],
                        profile_pic_url=api.LastJson['user']['profile_pic_url'],
                        is_verified=api.LastJson['user']['is_verified'],
                        follower_count=api.LastJson['user']['follower_count'],
                        following_count=api.LastJson['user']['following_count'],
                        biography=api.LastJson['user']['biography'],
                        feed=get_user_feed(api.LastJson['user']['pk'])
                        )

    raise GraphQLError(UNKNOW_ERROR)


def get_followers(api, next_page):
    if api.getUserFollowers(api.username_id, next_page):
        users = api.LastJson['users']
        next_page = api.LastJson['next_max_id']
        return users, next_page
    else:
        response = api.LastJson
        if response['message'] == MESSAGE_ERROR:
            raise GraphQLError(TOO_MANY_REQUESTS)

    raise GraphQLError(UNKNOW_ERROR)


def get_followings(api, next_page):
    if api.getUserFollowings(api.username_id, next_page):
        users = api.LastJson['users']
        next_page = api.LastJson['next_max_id']
        return users, next_page
    else:
        response = api.LastJson
        if response['message'] == MESSAGE_ERROR:
            raise GraphQLError(TOO_MANY_REQUESTS)

    raise GraphQLError(UNKNOW_ERROR)


def get_unfollowers(api):
    lst_pks = []
    lst_unfollowers = []

    try:
        lst_followings = api.getTotalFollowings(api.username_id)
        lst_followers = api.getTotalFollowers(api.username_id)
    except Exception:
        pass

    if api.LastJson['status'] == 'fail':
        if api.LastJson['message'] == MESSAGE_ERROR:
            raise GraphQLError(TOO_MANY_REQUESTS)

        print(api.LastJson['message'])
        raise GraphQLError(UNKNOW_ERROR)

    for user in lst_followers:
        lst_pks.append(user['pk'])

    for following in lst_followings:
        if following['pk'] not in lst_pks:
            lst_unfollowers.append(following)

    return lst_unfollowers


def get_user_feed(username_id, next_page=''):
    api = get_session(username_id)
    if api.getUserFeed(username_id, next_page):
        print(api.LastJson)
        response = api.LastJson['items']
        print(list(response.keys()))

        pictures = []

        for item in response:
            if "carousel_media" in list(item.keys()):
                url = item["carousel_media"][0]["image_versions2"]["candidates"][0]["url"]
            else:
                url = item["image_versions2"]["candidates"][0]["url"]

            pictures.append(
                Picture(
                    pk=item['pk'],
                    comment_count=item['comment_count'],
                    like_count=item['like_count'],
                    url=url
                ))

        return Feed(pictures=pictures, next_page=response['items']["next_max_id"], size=len(pictures))

    raise GraphQLError(UNKNOW_ERROR)


def get_user_followers_or_followings(type_user, current_pk, max_id):
    api = get_session(current_pk)

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
        if response['message'] == MESSAGE_ERROR:
            raise GraphQLError(TOO_MANY_REQUESTS)

    raise GraphQLError(UNKNOW_ERROR)


def get_not_followers(current_pk):
    lst_not_followers = []
    lst_followers = []
    lst_following = []

    api = get_session(current_pk)

    try:
        lst_following = api.getTotalFollowings(current_pk)
        response = api.getTotalFollowers(current_pk)
    except Exception:
        pass

    if api.LastJson['status'] == 'fail':
        if api.LastJson['message'] == MESSAGE_ERROR:
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
    api = get_session(current_pk)
    if api.unfollow(pk):
        return UNFOLLOW_SUCCESS

    raise GraphQLError(UNFOLLOW_ERROR)


def follow(current_pk, pk):
    api = get_session(current_pk)
    if api.follow(pk):
        return FOLLOW_SUCCESS

    raise GraphQLError(FOLLOW_ERROR)
