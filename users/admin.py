from django.contrib import admin
from users import models
from django.contrib.auth.models import Group
admin.site.unregister(Group)


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name',)
    search_fields = ('id', 'username', 'first_name', 'last_name',)
    list_per_page = 100



