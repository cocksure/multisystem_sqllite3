def can_sign_purchase(user):
    return user.is_authenticated and user.can_sign_purchase


def can_assign_purchase(user):
    return user.is_authenticated and user.can_assign_purchase


def is_admin(user):
    return user.is_authenticated and user.is_admin
