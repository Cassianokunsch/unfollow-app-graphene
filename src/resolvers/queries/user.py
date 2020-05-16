from graphene import ObjectType, Field, NonNull, String
from shared.utils import get_current_user
from resolvers.types.user_info import UserInfo
from resolvers.types.feed import Feed
from resolvers.types.my_unfollowers import MyUnfollowers
from resolvers.types.my_followers import MyFollowers
from resolvers.types.my_followings import MyFollowings
from service.user import get_user_info, get_user_feed, get_user_followers_or_followings, get_not_followers


class UserQuery(ObjectType):
    user_info = Field(NonNull(UserInfo), pk=String(default_value=''))

    user_feed = Field(NonNull(Feed), user_id=String(
        default_value=''), next_page=String(default_value=''))

    my_followers = Field(NonNull(MyFollowers),
                         next_page=String(default_value=''))

    my_followings = Field(NonNull(MyFollowings),
                          next_page=String(default_value=''))

    my_unfollowers = Field(NonNull(MyUnfollowers),
                           next_page=String(default_value=''))

    def resolve_user_info(self, info, pk):
        user_pk = get_current_user(info.context)
        return get_user_info(user_pk, pk)

    def resolve_user_feed(self, info, user_id, next_page):
        user_pk = get_current_user(info.context)
        return get_user_feed(user_pk, next_page)

    def resolve_my_followings(self, info, next_page):
        user_pk = get_current_user(info.context)
        users, next_page = get_user_followers_or_followings(
            'followings', user_pk, next_page)
        return MyFollowings(followings=users, next_page=next_page, size=len(users))

    def resolve_my_followers(self, info, next_page):
        user_pk = get_current_user(info.context)
        users, next_page = get_user_followers_or_followings(
            'followers', user_pk, next_page)
        return MyFollowers(followers=users, next_page=next_page, size=len(users))

    def resolve_my_unfollowers(self, info, next_page):
        user_pk = get_current_user(info.context)
        users = get_not_followers(user_pk)
        return MyUnfollowers(unfollowers=users, next_page="", size=len(users))
