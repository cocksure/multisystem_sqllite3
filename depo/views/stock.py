from rest_framework import generics

from depo import models, serializers
from shared.views import BaseListView


class StockListView(BaseListView):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer
    filterset_fields = ['warehouse']
    search_fields = ['material']


class StockDetailView(generics.RetrieveAPIView):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer
