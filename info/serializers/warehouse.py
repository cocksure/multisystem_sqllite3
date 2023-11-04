from info import models
from shared.serializers import BaseNameCodeSerializer


class WarehouseSerializer(BaseNameCodeSerializer):
    class Meta:
        model = models.Warehouse
        fields = '__all__'