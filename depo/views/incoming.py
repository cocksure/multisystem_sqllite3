from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import status, generics
from rest_framework.response import Response

from depo import serializers, models
from depo.models import Stock
from shared.views import BaseListView


# ---------------------------------------------------------------------------------------
class IncomingCreateView(generics.CreateAPIView):
    queryset = models.Incoming.objects.all()
    serializer_class = serializers.IncomingSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        incoming_data = request.data
        incoming_material_data = incoming_data.pop('incoming_materials', [])

        incoming_serializer = self.get_serializer(data=incoming_data)
        incoming_serializer.is_valid(raise_exception=True)
        incoming = incoming_serializer.save()

        for item in incoming_material_data:
            item['incoming'] = incoming.id

        incoming_material_serializer = serializers.IncomingMaterialSerializer(data=incoming_material_data, many=True)
        if incoming_material_serializer.is_valid():
            incoming_material_serializer.save()

            for item in incoming_material_data:
                material = item['material']
                amount = item['amount']
                warehouse = incoming.warehouse

                stock, created = Stock.objects.get_or_create(material=material, warehouse=warehouse)
                stock.amount += amount
                stock.save()

            try:
                incoming.full_clean()
            except ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            headers = self.get_success_headers(incoming_serializer.data)
            return Response(incoming_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(incoming_material_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------------------
class IncomingListView(BaseListView):
    queryset = models.Incoming.objects.all()
    serializer_class = serializers.IncomingSerializer
    filterset_fields = ['warehouse']
    search_fields = ['code']


# ---------------------------------------------------------------------------------------
class IncomingMaterialListView(generics.ListAPIView):
    queryset = models.IncomingMaterial.objects.all()
    serializer_class = serializers.IncomingMaterialSerializer


# ---------------------------------------------------------------------------------------

class IncomingDetailView(generics.RetrieveAPIView):
    queryset = models.Incoming.objects.all()
    serializer_class = serializers.IncomingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data

        incoming_materials = models.IncomingMaterial.objects.filter(incoming=instance)
        incoming_material_serializer = serializers.IncomingMaterialSerializer(incoming_materials, many=True)

        data['incoming_materials'] = incoming_material_serializer.data

        return Response(data)

# ---------------------------------------------------------------------------------------
