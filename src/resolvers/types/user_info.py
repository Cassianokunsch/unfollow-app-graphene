from graphene import ObjectType, String, Int, Field
from resolvers.types.user_interface import UserInterface
from resolvers.types.feed import Feed
#from shared.utils import get_current_user
#from storage.session import get_session
#from service.user import get_user_feed


class UserInfo(ObjectType):
    class Meta:
        interfaces = (UserInterface, )

    follower_count = Int()
    following_count = Int()
    biography = String()
    feed = Field(Feed)

    # def resolve_feed(self, info):
    #     print("teste")
    #     user_pk = get_current_user(info.context)
    #     return get_user_feed(user_pk)
