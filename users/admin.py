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
    list_display = ('username', 'first_name', 'last_name',)
    search_fields = ('id', 'username', 'first_name', 'last_name',)
    list_per_page = 100

    form = CustomUserChangeForm





