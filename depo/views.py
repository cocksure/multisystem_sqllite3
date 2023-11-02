from rest_framework import generics
from depo import models
from depo import serializers
from shared.views import BaseListView


class OutgoingListCreateView(BaseListView):
    queryset = models.Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer
    filterset_fields = ['warehouse', 'type', ]
    search_fields = ['code']


class OutgoingDetailListCreateView(BaseListView):
    queryset = models.OutgoingDetail.objects.all()
    serializer_class = serializers.DetailOutgoingSerializer


class IncomingListCreateView(BaseListView):
    queryset = models.Incoming.objects.all()
    serializer_class = serializers.IncomingSerializer
    filterset_fields = ['warehouse']
    search_fields = ['code']


class IncomingDetailListCreateView(BaseListView):
    queryset = models.IncomingDetail.objects.all()
    serializer_class = serializers.IncomingDetailSerializer


class OutgoingUpdateDeleteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer


class OutgoingDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.OutgoingDetail.objects.all()
    serializer_class = serializers.DetailOutgoingSerializer


class IncomingUpdateDeleteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Incoming.objects.all()
    serializer_class = serializers.IncomingSerializer


class IncomingDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.IncomingDetail.objects.all()
    serializer_class = serializers.IncomingDetailSerializer
