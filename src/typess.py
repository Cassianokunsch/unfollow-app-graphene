from graphene import ObjectType, Interface, String, Int, Boolean


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
