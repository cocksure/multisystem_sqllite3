from django.contrib import admin
from depo.models import outgoing, incoming, stock


@admin.register(outgoing.Outgoing)
class OutgoingAdmin(admin.ModelAdmin):
    list_display = ('code', 'warehouse', 'to_warehouse', 'outgoing_type', 'data',)
    list_filter = ('outgoing_type', 'warehouse',)
    readonly_fields = ('outgoing_type', 'code', 'status')

    search_fields = ('code',)
    fields = (
        'code', 'data', 'warehouse', 'to_warehouse', 'outgoing_type', 'status', 'note', 'created_by', 'updated_by',
        'created_time', 'updated_time')

    list_per_page = 100
    date_hierarchy = 'created_time'


@admin.register(outgoing.OutgoingMaterial)
class OutgoingMaterialAdmin(admin.ModelAdmin):
    list_display = ('outgoing', 'material', 'amount', 'color', 'material_party',)
    search_fields = ('material', 'material_party')
    readonly_fields = ('amount',)
    list_per_page = 100


@admin.register(incoming.Incoming)
class IncomingAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'from_warehouse', 'outgoing', 'data',)
    fields = (
        'data', 'warehouse', 'from_warehouse', 'type', 'invoice', 'contract_number', 'outgoing', 'purchase',
        'note', 'updated_by', 'created_time', 'updated_time')
    readonly_fields = ('type',)
    list_filter = ('warehouse',)
    search_fields = ('code',)
    list_per_page = 100
    date_hierarchy = 'created_time'


@admin.register(incoming.IncomingMaterial)
class IncomingDetailAdmin(admin.ModelAdmin):
    list_display = ('incoming', 'material', 'amount', 'color', 'material_party',)
    search_fields = ('material', 'material_party')
    readonly_fields = ('amount',)

    list_per_page = 100
    fields = ('incoming', 'material', 'amount', 'color', 'material_party',)


@admin.register(stock.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'material', 'amount', 'material__color__name')
    search_fields = ('material',)
    list_filter = ('warehouse',)
    list_per_page = 100
