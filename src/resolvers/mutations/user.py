from graphene import Mutation, String, NonNull
from service.user import unfollow, follow
from shared.utils import get_current_user


class Unfollow(Mutation):

    message = String()

    class Arguments:
        user_id_to_unfollow = String(required=True)

    def mutate(root, info, user_id_to_unfollow):
        user = get_current_user(info.context)
        message = unfollow(user, int(user_id_to_unfollow))
        print(message)
        return Unfollow(message=message)


class Follow(Mutation):

    message = String()

    class Arguments:
        user_id_to_follow = String(required=True)

    def mutate(root, info, user_id_to_follow):
        user = get_current_user(info.context)
        message = follow(user, int(user_id_to_follow))
        return Follow(message=message)
