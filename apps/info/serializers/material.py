from rest_framework.serializers import ModelSerializer
from apps.info import models
from apps.shared.serializers import BaseNameCodeSerializer


class MaterialSerializer(BaseNameCodeSerializer):
    class Meta:
        model = models.Material
        fields = ('id', 'code', 'name', 'type', 'group', 'unit', 'color',
                  'photo', 'price', 'note', 'warranty', 'size_and_shape', 'weight',
                  'created_time', 'updated_time', 'created_by', 'updated_by')


class MaterialPartySerializer(ModelSerializer):
    class Meta:
        model = models.MaterialParty
        fields = ('id', 'material', 'code')


class MaterialGroupSerializer(BaseNameCodeSerializer):
    class Meta:
        model = models.MaterialGroup
        fields = ('id', 'code', 'name')


class MaterialTypeSerializer(BaseNameCodeSerializer):
    class Meta:
        model = models.MaterialType
        fields = ('id', 'code', 'name')

