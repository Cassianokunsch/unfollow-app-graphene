from graphene import ObjectType, List, Field, NonNull, String
from instagramApi import get_total_followers, get_not_followers, get_total_followings
from utils import get_current_user
from typess import FollowerType, UnfollowerType, FollowingType, UserType


class Query(ObjectType):
    me = String()
    list_my_followers = List(NonNull(FollowerType))
    list_my_followings = List(NonNull(FollowingType))
    list_my_unfollowers = List(NonNull(UnfollowerType))

    def resolve_me(self, info):
        return "teste"

    def resolve_list_my_followers(self, info):
        user = get_current_user(info.context)
        return get_total_followers(user['id'])

    def resolve_list_my_followings(self, info):
        user = get_current_user(info.context)
        return get_total_followings(user['id'])

    def resolve_list_my_unfollowers(self, info):
        user = get_current_user(info.context)
        return get_not_followers(user['id'])
