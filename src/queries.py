from graphene import ObjectType, List, Field
from api.instagram import get_total_followers, get_not_followers, get_total_followings
from utils import get_current_user
from typess import FollowerType, UnfollowerType, FollowingType, UserType


class Query(ObjectType):
    me = Field(UserType)
    my_followers = List(FollowerType)
    my_following = List(FollowingType)
    my_unfollowers = List(UnfollowerType)

    def resolve_my_followers(self, info):
        user = get_current_user(info.context)
        return get_total_followers(user['id'])

    def resolve_my_following(self, info):
        user = get_current_user(info.context)
        return get_total_followings(user['id'])

    def resolve_my_unfollowers(self, info):
        user = get_current_user(info.context)
        return get_not_followers(user['id'])
