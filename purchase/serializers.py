from rest_framework.serializers import ModelSerializer
from purchase import models


class PurchaseSerializer(ModelSerializer):

    class Meta:
        model = models.Purchase
        fields = '__all__'


class PurchaseDetailSerializer(ModelSerializer):
    class Meta:
        model = models.PurchaseProduct
        fields = '__all__'

