from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'email', 'profile_image', 'is_active', 'can_sign_purchase',
            'is_staff', 'is_superuser',
            'groups', 'user_permissions')
