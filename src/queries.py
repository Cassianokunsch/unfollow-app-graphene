from graphene import ObjectType, Field, NonNull, String
from instagramApi import get_not_followers, get_user_info, get_user_followers_or_followings, get_me
from utils import get_current_user
from typess import UserType, MyFollowersType, MyFollowingsType, MyUnfollowersType, Feed
from auth import get_user_session


class Query(ObjectType):
    me = Field(NonNull(UserType))

    user_info = Field(NonNull(UserType), pk=String(required=True))

    my_followers = Field(
        NonNull(MyFollowersType), next_page=String(default_value=''))

    my_followings = Field(
        NonNull(MyFollowingsType), next_page=String(default_value=''))

    my_unfollowers = Field(NonNull(MyUnfollowersType),
                           next_page=String(default_value=''))

    feed_user = Field(Feed, user_id=String(default_value=''),
                      next_page=String(default_value=''))

    def resolve_feed_user(self, info, user_id, next_page):
        user_pk = get_current_user(info.context)
        user = get_user_session(user_pk)
        pictures, next_page = user.get_user_feed(user_id, next_page)
        return Feed(next_page=next_page, pictures=pictures, size=len(pictures))

    def resolve_me(self, info):
        user_pk = get_current_user(info.context)
        user = get_user_session(user_pk)
        return user.get_me()

    def resolve_user_info(self, info, pk):
        user_pk = get_current_user(info.context)
        return get_user_info(user_pk, pk)

    def resolve_my_followings(self, info, next_page):
        user_pk = get_current_user(info.context)
        users, next_page = get_user_followers_or_followings(
            'followings', user_pk, next_page)
        return MyFollowingsType(followings=users, next_page=next_page, size=len(users))

    def resolve_my_followers(self, info, next_page):
        user_pk = get_current_user(info.context)
        users, next_page = get_user_followers_or_followings(
            'followers', user_pk, next_page)
        return MyFollowersType(followers=users, next_page=next_page, size=len(users))

    def resolve_my_unfollowers(self, info, next_page):
        user_pk = get_current_user(info.context)
        users = get_not_followers(user_pk)
        return MyUnfollowersType(unfollowers=users, next_page=None, size=len(users))
