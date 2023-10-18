from rest_framework import generics
from purchase import models, serializers
from shared.models import BaseModel


class PurchaseListCreateView(BaseModel):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer


class PurchaseDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer


class PurchaseProductListCreateView(BaseModel):
    queryset = models.PurchaseProduct.objects.all()
    serializer_class = serializers.PurchaseDetailSerializer


class PurchaseProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.PurchaseProduct.objects.all()
    serializer_class = serializers.PurchaseDetailSerializer
