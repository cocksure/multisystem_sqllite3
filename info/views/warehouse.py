from rest_framework import generics
from info import models, serializers
from shared.views import BaseListView


class WarehouseListCreateView(BaseListView):
    queryset = models.Warehouse.objects.all()
    serializer_class = serializers.WarehouseSerializer
    filterset_fields = ['name']
    search_fields = ['code', 'name']


class WarehouseDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Warehouse.objects.all()
    serializer_class = serializers.WarehouseSerializer