def can_sign_purchase(user):
    return user.is_authenticated and user.can_sign_purchase


def can_assign_purchase(user):
    return user.is_authenticated and user.can_assign_purchase
