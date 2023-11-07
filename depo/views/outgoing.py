from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from depo import serializers, models
from depo.models import Stock
from info.models import Warehouse
from shared.views import BaseListView


class OutgoingListCreateView(BaseListView):
    queryset = models.Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer
    filterset_fields = ['warehouse', 'type']
    search_fields = ['code']


class OutgoingDetailListCreateView(BaseListView):
    queryset = models.OutgoingDetail.objects.all()
    serializer_class = serializers.DetailOutgoingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the outgoing detail
        outgoing_detail = serializer.save()

        material = outgoing_detail.material
        amount = outgoing_detail.amount
        outgoing = outgoing_detail.outgoing
        warehouse = get_object_or_404(Warehouse, id=outgoing.warehouse_id)

        if not warehouse.use_negative:
            # Check if stock will go negative without allowing negative stock
            stock, created = Stock.objects.get_or_create(material=material, warehouse=warehouse)
            if stock.amount < amount:
                return Response({"message": "Negative stock is not allowed for this warehouse."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Update the stock in the warehouse
        stock, _ = Stock.objects.get_or_create(material=material, warehouse=warehouse)
        stock.amount -= amount
        stock.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update_stock(self, material_id, warehouse, amount_change):
        stock, _ = Stock.objects.get_or_create(material=material_id, warehouse=warehouse)
        stock.amount -= amount_change
        stock.save()


