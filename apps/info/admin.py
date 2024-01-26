from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.info import models
from apps.info.resources import MaterialResource


@admin.register(models.Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('id', 'code', 'name')
    list_per_page = 100


@admin.register(models.Firm)
class FirmAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'phone_number', 'code', 'agent', 'created_by', 'created_time')
    search_fields = ('code', 'name')
    list_filter = ('type',)
    list_per_page = 100
    date_hierarchy = 'created_time'
    readonly_fields = (
        'created_time', 'updated_time', 'created_by', 'updated_by')
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'code', 'name', 'type', 'legal_address', 'actual_address', 'phone_number', 'fax_machine',
                'license_number',
                'agent',)
        }),
        ('Timestamps', {
            'fields': ('created_time', 'created_by', 'updated_time', 'updated_by'),
            'classes': ('collapse',),
        }),
    )


@admin.register(models.MaterialGroup)
class MaterialGroupAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    list_per_page = 100
    fields = ('code', 'name')


@admin.register(models.MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    list_per_page = 100
    fields = ('code', 'name')


@admin.register(models.Material)
class MaterialAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'code', 'group', 'type', 'unit')
    search_fields = ('code', 'name', 'group__name', 'type__name', 'unit__name')
    list_filter = ('group', 'type', 'unit')
    list_per_page = 100
    date_hierarchy = 'created_time'
    readonly_fields = ('created_time', 'updated_time')

    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'group', 'type', 'unit', 'color', 'photo', 'price', 'weight')
        }),
        ('Additional Information', {
            'fields': ('warranty', 'size_and_shape', 'note',)
        }),
        ('Timestamps', {
            'fields': ('created_time', 'created_by', 'updated_time', 'updated_by'),
            'classes': ('collapse',),
        }),
    )

    resource_class = MaterialResource


@admin.register(models.MaterialParty)
class MaterialPartyAdmin(admin.ModelAdmin):
    list_display = ('material', 'code')
    search_fields = ('material', 'code')
    list_per_page = 100


@admin.register(models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'location', 'can_import', 'can_export', 'use_negative', 'is_active')
    search_fields = ('code', 'name', 'location')
    list_filter = ('can_import', 'can_export', 'use_negative', 'is_active')
    list_per_page = 100
    date_hierarchy = 'created_time'
    readonly_fields = ('created_time', 'updated_time')

    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'location', 'can_import', 'can_export', 'use_negative', 'is_active', 'managers')
        }),

        ('Timestamps', {
            'fields': ('created_time', 'created_by', 'updated_time', 'updated_by'),
            'classes': ('collapse',),
        }),
    )


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('agent', 'imei', 'comment')
    search_fields = ('agent', 'imei')
    list_per_page = 100
    date_hierarchy = 'created_time'
    readonly_fields = ('created_time', 'updated_time')
    fields = ('agent', 'imei', 'comment', 'created_by', 'updated_by',)


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)
    search_fields = ('code', 'name')
    list_per_page = 100
    date_hierarchy = 'created_time'
    fields = ('code', 'name', 'created_by', 'updated_by', 'created_time', 'updated_time')
    readonly_fields = ('created_time', 'updated_time')


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name')
    list_per_page = 100
    date_hierarchy = 'created_time'
    fields = ('name', 'created_by', 'updated_by', 'created_time', 'updated_time')
    readonly_fields = ('created_time', 'updated_time')


@admin.register(models.Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'firm')
    search_fields = ('id', 'name', 'firm')
    list_per_page = 100
    date_hierarchy = 'created_time'
    readonly_fields = ('created_time', 'updated_time')
    fields = ('name', 'year', 'firm', 'created_by', 'updated_by',)
