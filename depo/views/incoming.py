from rest_framework import generics, status
from rest_framework.response import Response

from depo import serializers, models
from depo.models import Stock
from info.models import Warehouse
from shared.views import BaseListView
from django.shortcuts import get_object_or_404


class IncomingListCreateView(BaseListView):
    queryset = models.Incoming.objects.all()
    serializer_class = serializers.IncomingSerializer
    filterset_fields = ['warehouse']
    search_fields = ['code']


class IncomingDetailListCreateView(BaseListView):
    queryset = models.IncomingDetail.objects.all()
    serializer_class = serializers.IncomingDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Создать деталь прихода
        self.perform_create(serializer)

        # Обновить остатки на складе на основе информации о детали прихода
        material_id = serializer.validated_data['material']
        amount = serializer.validated_data['amount']
        incoming = serializer.validated_data['incoming']
        warehouse = get_object_or_404(Warehouse, id=incoming.warehouse_id)

        # Обновить остатки на складе на основе информации о детали прихода
        self.update_stock(material_id, warehouse, amount)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update_stock(self, material_id, warehouse, amount_change):
        stock, _ = Stock.objects.get_or_create(material=material_id, warehouse=warehouse)
        stock.amount += amount_change
        stock.save()


class IncomingUpdateDeleteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Incoming.objects.all()
    serializer_class = serializers.IncomingSerializer


class IncomingDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.IncomingDetail.objects.all()
    serializer_class = serializers.IncomingDetailSerializer
