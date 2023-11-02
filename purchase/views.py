from rest_framework import generics
from purchase import models, serializers
from rest_framework.response import Response
from rest_framework import status

from shared.filters import PurchaseFilter
from shared.views import BaseListView


class PurchaseListCreateView(BaseListView):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer
    filterset_fields = ['status']
    search_fields = ['id', 'requester']
    filterset_class = PurchaseFilter


class PurchaseDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer


class PurchaseProductListCreateView(generics.ListCreateAPIView):
    queryset = models.PurchaseProduct.objects.all()
    serializer_class = serializers.PurchaseDetailSerializer

    def create(self, request, *args, **kwargs):
        purchase_id = self.kwargs['purchase_id']

        try:
            purchase = models.Purchase.objects.get(pk=purchase_id)
        except models.Purchase.DoesNotExist:
            return Response({'error': 'Purchase not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(purchase=purchase)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.PurchaseProduct.objects.all()
    serializer_class = serializers.PurchaseDetailSerializer
