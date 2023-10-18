from django.contrib import admin
from depo import models


@admin.register(models.Outgoing)
class OutgoingAdmin(admin.ModelAdmin):
    list_display = ('code', 'warehouse', 'to_warehouse', 'type', 'data',)
    list_filter = ('type', 'warehouse',)
    search_fields = ('code',)
    fields = ('data', 'type', 'warehouse', 'to_warehouse',  'note', 'created_by', 'updated_by', 'created_time', 'updated_time' )
    list_per_page = 100
    date_hierarchy = 'created_time'


@admin.register(models.Incoming)
class IncomingAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'from_warehouse', 'outgoing', 'data',)
    list_filter = ('warehouse',)
    search_fields = ('code',)


@admin.register(models.IncomingDetail)
class IncomingDetailAdmin(admin.ModelAdmin):
    list_display = ('incoming', 'material', 'amount', 'color', 'material_party',)


@admin.register(models.DetailOutgoing)
class DetailOutgoingAdmin(admin.ModelAdmin):
    list_display = ('outgoing', 'material', 'amount', 'color', 'material_party',)
