from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import status, generics
from rest_framework.response import Response

from depo import serializers
from depo.models.outgoing import Outgoing, OutgoingMaterial
from depo.models.stock import Stock
from info.models import Warehouse
from shared.views import BaseListView


# ---------------------------------------------------------------------------------------
class OutgoingCreateView(generics.CreateAPIView):
    queryset = Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer

    def create(self, request, *args, **kwargs):
        outgoing_data = request.data
        outgoing_material_data = outgoing_data.pop('outgoing_materials', [])

        outgoing_serializer = self.get_serializer(data=outgoing_data)
        outgoing_serializer.is_valid(raise_exception=True)
        outgoing = outgoing_serializer.save()

        for item in outgoing_material_data:
            item['outgoing'] = outgoing.id

        outgoing_material_serializer = serializers.OutgoingMaterialSerializer(data=outgoing_material_data, many=True)
        if outgoing_material_serializer.is_valid():
            outgoing_material_serializer.save()

        try:
            outgoing.full_clean()
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            for item in outgoing_material_data:
                material = item['material']
                amount = item['amount']
                warehouse_id = outgoing_data.get('warehouse')

                stock, created = Stock.objects.get_or_create(material=material, warehouse=outgoing.warehouse)
                stock.amount -= amount
                stock.save()

        headers = self.get_success_headers(outgoing_serializer.data)
        return Response(outgoing_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# ---------------------------------------------------------------------------------------
class OutgoingListView(BaseListView):
    queryset = Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer
    filterset_fields = ['warehouse', 'type']
    search_fields = ['code']


# ---------------------------------------------------------------------------------------

class OutgoingMaterialListView(generics.ListAPIView):
    queryset = OutgoingMaterial.objects.all()
    serializer_class = serializers.OutgoingMaterialSerializer


# ---------------------------------------------------------------------------------------

class OutgoingDetailView(generics.RetrieveAPIView):
    queryset = Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data

        outgoing_materials = OutgoingMaterial.objects.filter(outgoing=instance)
        outgoing_material_serializer = serializers.OutgoingMaterialSerializer(outgoing_materials, many=True)

        data['outgoing_materials'] = outgoing_material_serializer.data

        return Response(data)

# ---------------------------------------------------------------------------------------
