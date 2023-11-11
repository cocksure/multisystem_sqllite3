from django.db import transaction
from rest_framework import status, generics
from rest_framework.response import Response

from depo import serializers, models
from depo.models import Stock, Incoming
from info.models import Warehouse
from shared.views import BaseListView
from django.shortcuts import get_object_or_404


# ---------------------------------------------------------------------------------------

class IncomingListView(BaseListView):
    queryset = models.Incoming.objects.all()
    serializer_class = serializers.IncomingSerializer
    filterset_fields = ['warehouse']
    search_fields = ['code']


# ---------------------------------------------------------------------------------------

class IncomingMaterialListView(generics.ListAPIView):
    queryset = models.IncomingMaterial.objects.all()
    serializer_class = serializers.IncomingMaterialSerializer


# ---------------------------------------------------------------------------------------


class IncomingCreateView(generics.CreateAPIView):
    queryset = models.IncomingMaterial.objects.all()
    serializer_class = serializers.IncomingMaterialSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        material_id = serializer.validated_data['material']
        amount = serializer.validated_data['amount']
        incoming = serializer.validated_data['incoming']
        warehouse = get_object_or_404(Warehouse, id=incoming.warehouse_id)

        self.update_stock(material_id, warehouse, amount)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update_stock(self, material_id, warehouse, amount_change):
        stock, _ = Stock.objects.get_or_create(material=material_id, warehouse=warehouse)
        stock.amount += amount_change
        stock.save()

# ---------------------------------------------------------------------------------------
