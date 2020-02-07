from graphene import ObjectType, Interface, String, Int, Boolean, List


class Payload(ObjectType):
    token = String()


class UserType(ObjectType):
    pk = String()
    username = String()
    full_name = String()
    is_private = Boolean()
    profile_pic_url = String()
    profile_pic_id = String()
    is_verified = Boolean()
    has_anonymous_profile_picture = Boolean()
    latest_reel_media = Int()
    follower_count = Int()
    following_count = Int()
    biography = String()


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


class FollowerType(ObjectType):
    class Meta:
        interfaces = (FollowUser, )


class UnfollowerType(ObjectType):
    class Meta:
        interfaces = (FollowUser, )


class FollowingType(ObjectType):
    class Meta:
        interfaces = (FollowUser, )


class MyFollowersResponse(ObjectType):
    next_max_id = String()
    followers = List(FollowerType)


class MyFollowingsResponse(ObjectType):
    next_max_id = String()
    followings = List(FollowingType)


class MyUnfollowersResponse(ObjectType):
    next_max_id = String()
    unfollowers = List(UnfollowerType)
