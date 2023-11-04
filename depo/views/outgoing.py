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

        # Создать деталь расхода
        self.perform_create(serializer)

        # Обновить остатки на складе на основе информации о детали расхода
        material_id = serializer.validated_data['material']
        amount = serializer.validated_data['amount']
        outgoing = serializer.validated_data['outgoing']
        warehouse = get_object_or_404(Warehouse, id=outgoing.warehouse_id)

        # Обновить остатки на складе на основе информации о детали расхода
        self.update_stock(material_id, warehouse, amount)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update_stock(self, material_id, warehouse, amount_change):
        stock, _ = Stock.objects.get_or_create(material=material_id, warehouse=warehouse)
        stock.amount -= amount_change
        stock.save()


class OutgoingUpdateDeleteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer


class OutgoingDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.OutgoingDetail.objects.all()
    serializer_class = serializers.DetailOutgoingSerializer
