from rest_framework.serializers import ModelSerializer
from purchase import models


class PurchaseListOnlySerializer(ModelSerializer):
    class Meta:
        model = models.Purchase
        fields = '__all__'


class PurchaseProductSerializer(ModelSerializer):
    class Meta:
        model = models.PurchaseProduct
        fields = '__all__'


class PurchaseSerializer(ModelSerializer):
    purchase_products = PurchaseProductSerializer(many=True, read_only=True)

    class Meta:
        model = models.Purchase
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        purchase_products = models.PurchaseProduct.objects.filter(purchase=instance)
        purchase_products_data = PurchaseProductSerializer(purchase_products, many=True).data
        data['purchase_products'] = purchase_products_data

        return data

