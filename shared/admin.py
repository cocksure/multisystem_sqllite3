from django.contrib import admin

from shared.models import SubMenu, MainMenu


class SubMenuInline(admin.TabularInline):
    model = SubMenu
    extra = 1


@admin.register(MainMenu)
class MainMenuAdmin(admin.ModelAdmin):
    inlines = [SubMenuInline]


admin.site.register(SubMenu)
