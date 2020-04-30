from graphene import ObjectType, Field, NonNull, String
from service.instagramApi import get_user_info
from shared.utils import get_current_user
from resolvers.types.types import UserType, Feed
from middleware.auth import get_user_session


class FriendsQuery(ObjectType):

    user_info = Field(NonNull(UserType), pk=String(required=True))

    feed_user = Field(Feed, user_id=String(default_value=''),
                      next_page=String(default_value=''))

    def resolve_feed_user(self, info, user_id, next_page):
        user_pk = get_current_user(info.context)
        user = get_user_session(user_pk)
        pictures, next_page = user.get_user_feed(user_id, next_page)
        return Feed(next_page=next_page, pictures=pictures, size=len(pictures))

    def resolve_user_info(self, info, pk):
        user_pk = get_current_user(info.context)
        return get_user_info(user_pk, pk)
