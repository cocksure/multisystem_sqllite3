from rest_framework.serializers import ModelSerializer
from info import models


class SpecSerializer(ModelSerializer):
    class Meta:
        model = models.Specification
        fields = '__all__'


class UnitSerializer(ModelSerializer):
    class Meta:
        model = models.Unit
        fields = '__all__'


class FirmSerializer(ModelSerializer):
    class Meta:
        model = models.Firm
        fields = '__all__'


class MaterialGroupSerializer(ModelSerializer):
    class Meta:
        model = models.MaterialGroup
        fields = '__all__'


class MaterialSerializer(ModelSerializer):
    class Meta:
        model = models.Material
        fields = '__all__'


class MaterialTypeSerializer(ModelSerializer):
    class Meta:
        model = models.MaterialType
        fields = '__all__'


class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = models.Warehouse
        fields = '__all__'


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = models.Device
        fields = '__all__'


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = models.Currency
        fields = '__all__'


class DealerSerializer(ModelSerializer):
    class Meta:
        model = models.Dealer
        fields = '__all__'


class BrandSerializer(ModelSerializer):
    class Meta:
        model = models.Brand
        fields = '__all__'
