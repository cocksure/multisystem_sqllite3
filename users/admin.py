from django.contrib import admin
from users import models
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialApp, SocialToken, SocialAccount
from django.contrib.sites.models import Site


from users.forms import CustomUserChangeForm

admin.site.unregister(Group)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(Site)
admin.site.unregister(SocialAccount)


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Custom Permissions', {'fields': ('can_sign_purchase',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'can_sign_purchase')
    search_fields = ('id', 'username', 'first_name', 'last_name',)
    list_filter = ('can_sign_purchase',)
    list_per_page = 100





