from graphene import Interface, String, Int, Boolean


class UserInterface(Interface):
    pk = String()
    username = String()
    full_name = String()
    is_private = Boolean()
    profile_pic_url = String()
    is_verified = Boolean()
