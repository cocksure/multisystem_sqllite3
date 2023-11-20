from django.contrib import admin
from depo.models import outgoing, incoming, stock


@admin.register(outgoing.Outgoing)
class OutgoingAdmin(admin.ModelAdmin):
    list_display = ('code', 'warehouse', 'to_warehouse', 'outgoing_type', 'data',)
    list_filter = ('outgoing_type', 'warehouse',)
    search_fields = ('code',)
    fields = ('data', 'outgoing_type', 'warehouse', 'to_warehouse', 'note', 'created_by', 'updated_by',
              'created_time', 'updated_time')
    list_per_page = 100
    date_hierarchy = 'created_time'


@admin.register(outgoing.OutgoingMaterial)
class OutgoingMaterialAdmin(admin.ModelAdmin):
    list_display = ('outgoing', 'material', 'amount', 'color', 'material_party',)
    search_fields = ('material', 'material_party')
    list_per_page = 100


@admin.register(incoming.Incoming)
class IncomingAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'from_warehouse', 'outgoing', 'data',)
    list_filter = ('warehouse',)
    search_fields = ('code',)
    list_per_page = 100
    date_hierarchy = 'created_time'


@admin.register(incoming.IncomingMaterial)
class IncomingDetailAdmin(admin.ModelAdmin):
    list_display = ('incoming', 'material', 'amount', 'color', 'material_party',)
    search_fields = ('material', 'material_party')
    list_per_page = 100
    fields = ('incoming', 'material', 'amount', 'color', 'material_party',)


@admin.register(stock.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'material', 'amount')
    search_fields = ('material',)
    list_filter = ('warehouse',)
    list_per_page = 100
