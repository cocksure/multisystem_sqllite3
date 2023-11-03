from rest_framework import generics

from depo import serializers, models
from shared.views import BaseListView


class OutgoingListCreateView(BaseListView):
    queryset = models.Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer
    filterset_fields = ['warehouse', 'type', ]
    search_fields = ['code']


class OutgoingDetailListCreateView(BaseListView):
    queryset = models.OutgoingDetail.objects.all()
    serializer_class = serializers.DetailOutgoingSerializer


class OutgoingUpdateDeleteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer


class OutgoingDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.OutgoingDetail.objects.all()
    serializer_class = serializers.DetailOutgoingSerializer
