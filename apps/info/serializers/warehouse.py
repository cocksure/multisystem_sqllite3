from rest_framework import serializers

from apps.info import models
from apps.shared.serializers import BaseNameCodeSerializer


class WarehouseSerializer(BaseNameCodeSerializer):
    class Meta:
        model = models.Warehouse
        fields = '__all__'

    def validate(self, data):
        if not data.get('is_active'):
            raise serializers.ValidationError("Склад неактивен.")
        if not data.get('can_import'):
            raise serializers.ValidationError("Склад не может импортировать!")
        if not data.get('can_export'):
            raise serializers.ValidationError("Warehouse cannot export products.")
        if data.get('use_negative') and data.get('available_quantity') < 0:
            raise serializers.ValidationError("На складе отрицательный запас.")
        return data
