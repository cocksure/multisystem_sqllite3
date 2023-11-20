from rest_framework.generics import ListAPIView, RetrieveAPIView

from depo import serializers
from depo.models.outgoing import OutgoingMaterial, Outgoing
from depo.models.stock import Stock
from shared.utils import CustomPagination
from shared.views import BaseListView

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from depo.serializers import StockSerializer, OutgoingMaterialSerializer, OutgoingSerializer


# ----------------------------------------------------------------------------------------
class StockListView(BaseListView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filterset_fields = ['material__group', 'warehouse']
    search_fields = ['material__name', 'material_party']
    pagination_class = CustomPagination

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        stock = self.get_object()
        self.check_object_permissions(self.request, stock)

        outgoing_transactions = OutgoingMaterial.objects.filter(
            material=stock.material,
            material_party=stock.material_party,
            status='В ожидании'
        )

        outgoing_serializer = OutgoingMaterialSerializer(outgoing_transactions, many=True)

        return Response({
            'outgoing_transactions': outgoing_serializer.data,
            'stock': StockSerializer(stock).data
        })


# ----------------------------------------------------------------------------------------
class StockDetailView(generics.RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = serializers.StockSerializer


# ----------------------------------------------------------------------------------------
class UnacceptedMaterialsListView(ListAPIView):
    serializer_class = OutgoingSerializer
    filterset_fields = ['warehouse']
    search_fields = [
        'outgoing_materials__material__name',
        'outgoing_materials__material_party__code'
    ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Outgoing.objects.filter(status='В ожидании')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OutgoingSerializer(queryset, many=True)
        return Response(serializer.data)


# ----------------------------------------------------------------------------------------
class UnacceptedMaterialsDetailView(RetrieveAPIView):
    queryset = Outgoing.objects.all()
    serializer_class = OutgoingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data

        outgoing_materials = OutgoingMaterial.objects.filter(
            outgoing=instance,
        )

        outgoing_material_serializer = OutgoingMaterialSerializer(outgoing_materials, many=True)
        data['outgoing_materials'] = outgoing_material_serializer.data

        return Response(data)

# ----------------------------------------------------------------------------------------
