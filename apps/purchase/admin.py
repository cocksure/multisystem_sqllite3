from django.contrib import admin

from apps.purchase import models


@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'requester', 'status', 'data', 'arrival_date')
    search_fields = ('id', 'requester')
    list_filter = ('department', 'status')


@admin.register(models.PurchaseProduct)
class PurchaseProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'material', 'color', 'status', 'specification')
    search_fields = ('id', 'material')
    list_filter = ('status',)
