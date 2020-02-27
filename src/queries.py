from graphene import ObjectType, List, Field, NonNull, String
from instagramApi import get_not_followers, get_user_info, get_user_followers_or_followings
from utils import get_current_user
from typess import UnfollowerType, UserType, MyFollowersResponse, MyFollowingsResponse


class Query(ObjectType):
    me = Field(NonNull(UserType))
    my_list_followers = Field(
        MyFollowersResponse, max_id=String(default_value=''))
    my_list_followings = Field(
        MyFollowingsResponse, max_id=String(default_value=''))
    my_list_unfollowers = List(NonNull(UnfollowerType))

    def resolve_me(self, info):
        user = get_current_user(info.context)
        return get_user_info(user)

    def resolve_my_list_followings(self, info, max_id):
        user = get_current_user(info.context)
        users, next_max_id = get_user_followers_or_followings(
            'followings', user, max_id)
        return MyFollowingsResponse(followings=users, next_max_id=next_max_id, size=len(users))

    def resolve_my_list_followers(self, info, max_id):
        user = get_current_user(info.context)
        users, next_max_id = get_user_followers_or_followings(
            'followers', user, max_id)
        return MyFollowersResponse(followers=users, next_max_id=next_max_id, size=len(users))

    def resolve_my_list_unfollowers(self, info):
        user = get_current_user(info.context)
        return get_not_followers(user)
