from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from depo import models, services


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

    def validate(self, data):
        incoming_type = data.get('type')
        invoice = data.get('invoice')
        if incoming_type == 'По накладной' and not invoice:
            raise serializers.ValidationError({'__all__': ['Необходимо указать номер инвойса.']})
        return data


class StockSerializer(ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)
    material_group = serializers.CharField(source='material.group.name', read_only=True)
    material_party = serializers.CharField(source='material.material_party.code', read_only=True)
    material_color = serializers.CharField(source='material.color', read_only=True)
    material_unit = serializers.CharField(source='material.unit.name', read_only=True)

    class Meta:
        model = models.Stock
        fields = ['id', 'warehouse', 'material_name', 'material_group',
                  'material_party', 'material_unit', 'material_color', 'amount']
