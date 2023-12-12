from rest_framework import viewsets
from info import models
from shared.utils import CustomPagination

from info.serializers import material


class MaterialGroupViewSetView(viewsets.ModelViewSet):
    queryset = models.MaterialGroup.objects.all()
    serializer_class = material.MaterialGroupSerializer
    search_fields = ['code', 'name']
    pagination_class = CustomPagination


class MaterialTypeViewSetView(viewsets.ModelViewSet):
    queryset = models.MaterialType.objects.all()
    serializer_class = material.MaterialTypeSerializer
    search_fields = ['code', 'name']
    pagination_class = CustomPagination


class MaterialViewSetView(viewsets.ModelViewSet):
    queryset = models.Material.objects.all()
    serializer_class = material.MaterialSerializer
    filterset_fields = ['group', 'type']
    search_fields = ['code', 'name']
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
