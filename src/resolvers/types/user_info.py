from graphene import ObjectType, String, Int, Field, NonNull
from resolvers.types.user_interface import UserInterface
from resolvers.types.feed import Feed


class UserInfo(ObjectType):
    class Meta:
        interfaces = (UserInterface, )

    follower_count = NonNull(Int)
    following_count = NonNull(Int)
    biography = NonNull(String)
    feed = Field(NonNull(Feed))
