from graphene import ObjectType, Interface, String, Int, Boolean, List, NonNull, Field


class FollowUser(Interface):
    pk = String()
    username = String()
    full_name = String()
    is_private = Boolean()
    profile_pic_url = String()
    profile_pic_id = String()
    is_verified = Boolean()
    has_anonymous_profile_picture = Boolean()
    latest_reel_media = Int()


class UserType(ObjectType):
    class Meta:
        interfaces = (FollowUser, )

    follower_count = Int()
    following_count = Int()
    biography = String()


class AuthPayload(ObjectType):
    message = NonNull(String)
    token = NonNull(String)


class FollowerType(ObjectType):
    class Meta:
        interfaces = (FollowUser, )


class UnfollowerType(ObjectType):
    class Meta:
        interfaces = (FollowUser, )


class FollowingType(ObjectType):
    class Meta:
        interfaces = (FollowUser, )


class MyFollowersType(ObjectType):
    next_page = String()
    size = Int()
    followers = List(FollowerType)


class MyFollowingsType(ObjectType):
    next_page = String()
    size = Int()
    followings = List(FollowingType)


class MyUnfollowersType(ObjectType):
    next_page = String()
    size = Int()
    unfollowers = List(UnfollowerType)
