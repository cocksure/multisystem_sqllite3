from rest_framework import viewsets
from info import models
from shared.utils import CustomPagination
from info.serializers import warehouse


class WarehouseViewSetView(viewsets.ModelViewSet):
    queryset = models.Warehouse.objects.all()
    serializer_class = warehouse.WarehouseSerializer
    filterset_fields = ['name']
    search_fields = ['code', 'name']
    pagination_class = CustomPagination
