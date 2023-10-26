from django.contrib import admin
from hr import models


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount_of_employee')
    list_per_page = 100


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 100


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'user', 'department', 'position', 'badge_number', 'report_card', 'is_fired',
                    'date_of_hire')
    list_filter = ('department', 'position', 'is_fired')
    search_fields = ('full_name', 'department', 'positions', 'badge_number', 'report_card',)
    date_hierarchy = 'created_time'
    list_per_page = 100
