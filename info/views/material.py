from rest_framework import generics
from info import models
from shared.views import BaseListView

from info.serializers import material


class MaterialGroupListCreateView(BaseListView):
    queryset = models.MaterialGroup.objects.all()
    serializer_class = material.MaterialGroupSerializer
    search_fields = ['code', 'name']


class MaterialTypeListCreateView(BaseListView):
    queryset = models.MaterialType.objects.all()
    serializer_class = material.MaterialTypeSerializer
    search_fields = ['code', 'name']


class MaterialListCreateView(BaseListView):
    queryset = models.Material.objects.all()
    serializer_class = material.MaterialSerializer
    filterset_fields = ['group', 'type']
    search_fields = ['code', 'name', 'material_party__code']


class MaterialDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Material.objects.all()
    serializer_class = material.MaterialSerializer


class MaterialGroupDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MaterialGroup.objects.all()
    serializer_class = material.MaterialGroupSerializer


class MaterialTypeDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MaterialType.objects.all()
    serializer_class = material.MaterialTypeSerializer
