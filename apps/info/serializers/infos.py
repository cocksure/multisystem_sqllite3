from rest_framework.serializers import ModelSerializer
from apps.info import models
from apps.shared.serializers import BaseNameCodeSerializer


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
        fields = ('id', 'code', 'name', 'type', 'legal_address', 'actual_address', 'phone_number',
                  'fax_machine', 'license_number', 'agent', 'created_by', 'updated_by', 'created_time',
                  'updated_time')


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
