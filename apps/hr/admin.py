from django.contrib import admin
from apps.hr import models


@admin.register(models.Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 100


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
    readonly_fields = (
        'created_time', 'updated_time', 'created_by', 'updated_by')
    fieldsets = (
        ('Личная Информация', {
            'fields': ('full_name', 'gender', 'date_of_birth', 'address', 'phone_number', 'email', 'photo')
        }),
        ('Информация о Трудоустройстве', {
            'fields': ('department', 'position', 'salary', 'date_of_hire', 'is_fired', 'date_of_fire', 'user', 'warehouses')
        }),
        ('Информация о Документах', {
            'fields': (
                'report_card', 'badge_number', 'passport_number_series', 'passport_issued_by', 'passport_when_issued',
                'passport_pin')
        }),
        ('Timestamps', {
            'fields': ('created_time', 'created_by', 'updated_time', 'updated_by'),
            'classes': ('collapse',),
        }),
    )
