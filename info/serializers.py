from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from info import models
from shared.serializers import BaseNameCodeSerializer


class MaterialPartySerializer(ModelSerializer):

    class Meta:
        model = models.MaterialParty
        fields = ('id', 'material', 'code')

class UnitSerializer(BaseNameCodeSerializer):
    class Meta:
        model = models.Unit
        fields = ('id', 'code', 'name')


class SpecSerializer(ModelSerializer):
    class Meta:
        model = models.Specification
        fields = '__all__'


class FirmSerializer(BaseNameCodeSerializer):
    class Meta:
        model = models.Firm
        fields = '__all__'


class MaterialGroupSerializer(BaseNameCodeSerializer):
    class Meta:
        model = models.MaterialGroup
        fields = '__all__'


class MaterialSerializer(BaseNameCodeSerializer):

    class Meta:
        model = models.Material
        fields = '__all__'




class MaterialTypeSerializer(BaseNameCodeSerializer):
    class Meta:
        model = models.MaterialType
        fields = '__all__'


class WarehouseSerializer(BaseNameCodeSerializer):
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



