from rest_framework import generics
from info import models
from shared.views import BaseListView
from info.serializers import warehouse


class WarehouseListCreateView(BaseListView):
    queryset = models.Warehouse.objects.all()
    serializer_class = warehouse.WarehouseSerializer
    filterset_fields = ['name']
    search_fields = ['code', 'name']


class WarehouseDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Warehouse.objects.all()
    serializer_class = warehouse.WarehouseSerializer
