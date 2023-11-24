from django.contrib import admin
from depo.models import outgoing, incoming, stock


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
        'data', 'warehouse', 'from_warehouse', 'type', 'invoice', 'contract_number', 'outgoing', 'purchase',
        'note', 'created_time', 'updated_time', 'created_by', 'updated_by', )
    readonly_fields = ('type', 'created_time', 'updated_time')
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
    list_display = ('warehouse', 'material_name', 'amount', 'unit_name', 'material_party', 'material_color', 'material_price')
    search_fields = ('material__name',)
    list_filter = ('warehouse',)
    list_per_page = 100

    def material_name(self, obj):
        return obj.material.name if obj.material else ''

    def unit_name(self, obj):
        return obj.material.unit.name if obj.material and obj.material.unit else ''

    def material_color(self, obj):
        return obj.material.color if obj.material and obj.material.color else ''

    def material_price(self, obj):
        return obj.material.price if obj.material and obj.material.price else ''
