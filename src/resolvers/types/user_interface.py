from graphene import Interface, String, Int, Boolean, NonNull


class UserInterface(Interface):
    pk = NonNull(String)
    username = NonNull(String)
    full_name = NonNull(String)
    is_private = NonNull(Boolean)
    profile_pic_url = NonNull(String)
    is_verified = NonNull(Boolean)
