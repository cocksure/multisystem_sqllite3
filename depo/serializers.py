from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from depo.models.incoming import IncomingMaterial, Incoming
from depo.models.outgoing import OutgoingMaterial, Outgoing
from depo.models.stock import Stock
from rest_framework.serializers import ValidationError as DRFValidationError


class OutgoingMaterialSerializer(ModelSerializer):
    class Meta:
        model = OutgoingMaterial
        fields = '__all__'


class OutgoingSerializer(ModelSerializer):
    class Meta:
        model = Outgoing
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        outgoing_materials = OutgoingMaterial.objects.filter(outgoing=instance)
        outgoing_material_data = OutgoingMaterialSerializer(outgoing_materials, many=True).data
        data['outgoing_materials'] = outgoing_material_data

        return data

    def validate(self, data):
        warehouse = data.get('warehouse')
        outgoing_type = data.get('outgoing_type')
        to_warehouse = data.get('to_warehouse')

        if outgoing_type == Outgoing.OutgoingType.MOVEMENT and not to_warehouse:
            raise DRFValidationError({'__all__': ['Выберите склад в поле "to_warehouse", так как тип - перемещения.']})
        if to_warehouse == warehouse:
            raise DRFValidationError({'__all__': ['Нельзя перемещать товары на тот же самый склад.']})

        # --------------------------------------------------------------------------------------------------------------
        if not warehouse.can_export:
            raise serializers.ValidationError('Невозможно провести расход. Склад не может экспортировать товары.')
        if not warehouse.is_active:
            raise serializers.ValidationError('Неактивный склад.')
        # --------------------------------------------------------------------------------------------------------------

        outgoing_materials = data.get('outgoing_materials', [])

        for material_data in outgoing_materials:
            material = material_data.get('material')
            amount = material_data.get('amount')

            if not material or not amount:
                raise serializers.ValidationError('Некорректные данные по исходящим материалам.')

            stock, created = Stock.objects.get_or_create(material=material, warehouse=warehouse)

            if not warehouse.use_negative and stock.amount < amount:
                raise serializers.ValidationError('Недостаточно товара на складе.')

        return data


class IncomingMaterialSerializer(ModelSerializer):
    class Meta:
        model = IncomingMaterial
        fields = '__all__'


class IncomingSerializer(serializers.ModelSerializer):
    incoming_materials = serializers.SerializerMethodField()

    class Meta:
        model = Incoming
        fields = '__all__'

    def get_incoming_materials(self, instance):
        incoming_materials = IncomingMaterial.objects.filter(incoming=instance)
        return IncomingMaterialSerializer(incoming_materials, many=True).data

    def validate(self, data):
        from_warehouse = data.get('from_warehouse')

        if from_warehouse:
            data['incoming_type'] = 'Перемешения'
        else:
            data['incoming_type'] = 'По накладной'

        incoming_type = data.get('incoming_type')
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
        model = Stock
        fields = ['id', 'warehouse', 'material_name', 'material_group',
                  'material_unit', 'material_color', 'amount']
