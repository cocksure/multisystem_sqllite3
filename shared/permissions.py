

def can_sign_purchase(user):
    return user.is_authenticated and user.can_sign_purchase
