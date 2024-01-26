from django.contrib import admin
from apps.depo.models import stock, incoming, outgoing


@admin.register(outgoing.Outgoing)
class OutgoingAdmin(admin.ModelAdmin):
    list_display = ('code', 'warehouse', 'to_warehouse', 'outgoing_type', 'data',)
    list_filter = ('outgoing_type', 'warehouse',)
    readonly_fields = ('outgoing_type', 'code', 'status', 'created_time', 'updated_time')

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
        'data', 'warehouse', 'from_warehouse', 'incoming_type', 'invoice', 'contract_number', 'outgoing', 'purchase',
        'note', 'created_time', 'updated_time', 'created_by', 'updated_by',)
    readonly_fields = ('incoming_type', 'created_time', 'updated_time')
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
    list_display = ('warehouse', 'material_name', 'amount')
    search_fields = ('material__name',)
    readonly_fields = ('warehouse', 'amount', 'material')
    list_filter = ('warehouse',)
    list_per_page = 100

    def has_delete_permission(self, request, obj=None):
        return False
    @staticmethod
    def material_name(obj):
        return obj.material.name if obj.material else ''
