from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response

from apps.depo import serializers
from apps.depo.models.incoming import Incoming, IncomingMaterial
from apps.depo.models.stock import Stock
from apps.depo.serializers import IncomingSerializer, IncomingMaterialSerializer
from apps.info.models import Warehouse
from apps.shared.utils import CustomPagination
from apps.shared.views import BaseListView


# ---------------------------------------------------------------------------------------
class IncomingCreateView(generics.CreateAPIView):
    queryset = Incoming.objects.all()
    serializer_class = IncomingSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        incoming_data = request.data.copy()
        incoming_material_data = incoming_data.pop('incoming_materials', [])

        warehouse_id = incoming_data.get('warehouse')
        warehouse = get_object_or_404(Warehouse, id=warehouse_id)

        if not request.user.is_authenticated or not warehouse.managers.filter(id=request.user.id).exists():
            raise PermissionDenied("У вас нет разрешения на выполнение операции прихода в этом складе.")

        incoming_data['created_by'] = request.user.id if request.user.is_authenticated else None
        incoming_data['data'] = timezone.now().date()

        incoming_serializer = self.get_serializer(data=incoming_data)
        incoming_serializer.is_valid(raise_exception=True)

        incoming = incoming_serializer.save()

        incoming_material_data = [{'incoming': incoming.id, **item} for item in incoming_material_data]
        incoming_material_serializer = IncomingMaterialSerializer(data=incoming_material_data, many=True)

        if incoming_material_serializer.is_valid():
            incoming_material_serializer.save()

            stocks_to_update = []
            for item in incoming_material_data:
                material = item['material']
                amount = item['amount']
                warehouse = incoming.warehouse

                stock, created = Stock.objects.get_or_create(material=material, warehouse=warehouse)
                stock.amount += amount
                stocks_to_update.append(stock)

            Stock.objects.bulk_update(stocks_to_update, ['amount'])

            headers = self.get_success_headers(incoming_serializer.data)
            return Response(incoming_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(incoming_material_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------------------
class IncomingListView(BaseListView):
    queryset = Incoming.objects.all()
    serializer_class = serializers.IncomingListOnlySerializer
    filterset_fields = ['warehouse']
    search_fields = ['code']
    pagination_class = CustomPagination


# ---------------------------------------------------------------------------------------
class IncomingMaterialListView(generics.ListAPIView):
    queryset = IncomingMaterial.objects.all()
    serializer_class = serializers.IncomingMaterialSerializer


# ---------------------------------------------------------------------------------------

class IncomingDetailView(generics.RetrieveAPIView):
    queryset = Incoming.objects.all().prefetch_related('incomingmaterial_set__material')
    serializer_class = serializers.IncomingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.validated_data

        incoming_materials = instance.incomingmaterial_set.all()
        incoming_material_serializer = serializers.IncomingMaterialSerializer(incoming_materials, many=True)

        data['incoming_materials'] = incoming_material_serializer.data

        return Response(data)

# ---------------------------------------------------------------------------------------
