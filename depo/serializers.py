from rest_framework.serializers import ModelSerializer
from depo import models


class OutgoingMaterialSerializer(ModelSerializer):
    class Meta:
        model = models.OutgoingMaterial
        fields = '__all__'


class OutgoingSerializer(ModelSerializer):
    class Meta:
        model = models.Outgoing
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Вычислите и добавьте связанные OutgoingMaterial в данные
        outgoing_materials = models.OutgoingMaterial.objects.filter(outgoing=instance)
        outgoing_material_data = OutgoingMaterialSerializer(outgoing_materials, many=True).data
        data['outgoing_materials'] = outgoing_material_data

        return data


class IncomingMaterialSerializer(ModelSerializer):
    class Meta:
        model = models.IncomingMaterial
        fields = '__all__'


class IncomingSerializer(ModelSerializer):
    class Meta:
        model = models.Incoming
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        incoming_materials = models.IncomingMaterial.objects.filter(incoming=instance)
        incoming_materials_data = IncomingMaterialSerializer(incoming_materials, many=True).data
        data['incoming_materials'] = incoming_materials_data

        return data


class StockSerializer(ModelSerializer):
    class Meta:
        model = models.Stock
        fields = '__all__'
