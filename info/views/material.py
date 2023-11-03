from rest_framework import generics
from info import models, serializers
from shared.views import BaseListView

from django.db.models import Q


class MaterialGroupListCreateView(BaseListView):
    queryset = models.MaterialGroup.objects.all()
    serializer_class = serializers.MaterialGroupSerializer
    search_fields = ['code', 'name']


class MaterialTypeListCreateView(BaseListView):
    queryset = models.MaterialType.objects.all()
    serializer_class = serializers.MaterialTypeSerializer
    search_fields = ['code', 'name']


class MaterialListCreateView(BaseListView):
    queryset = models.Material.objects.all()
    serializer_class = serializers.MaterialSerializer
    filterset_fields = ['group', 'type']
    search_fields = ['code', 'name', 'material_party__party__code']


class MaterialDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Material.objects.all()
    serializer_class = serializers.MaterialSerializer


class MaterialGroupDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MaterialGroup.objects.all()
    serializer_class = serializers.MaterialGroupSerializer


class MaterialTypeDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MaterialType.objects.all()
    serializer_class = serializers.MaterialTypeSerializer
