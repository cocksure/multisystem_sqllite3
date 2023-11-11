from rest_framework import status, generics
from rest_framework.response import Response

from depo import serializers, models
from depo.models import Stock
from shared.views import BaseListView

# ---------------------------------------------------------------------------------------


class OutgoingListView(BaseListView):
    queryset = models.Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer
    filterset_fields = ['warehouse', 'type']
    search_fields = ['code']


# ---------------------------------------------------------------------------------------

class OutgoingMaterialListView(generics.ListAPIView):
    queryset = models.OutgoingMaterial.objects.all()
    serializer_class = serializers.OutgoingMaterialSerializer


# ---------------------------------------------------------------------------------------
class OutgoingDetailView(generics.RetrieveAPIView):
    queryset = models.Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data

        # Filter the related OutgoingMaterial for the specific Outgoing instance
        outgoing_materials = models.OutgoingMaterial.objects.filter(outgoing=instance)
        outgoing_material_serializer = serializers.OutgoingMaterialSerializer(outgoing_materials, many=True)

        data['outgoing_materials'] = outgoing_material_serializer.data

        return Response(data)


# ---------------------------------------------------------------------------------------

class OutgoingCreateView(generics.CreateAPIView):
    queryset = models.Outgoing.objects.all()
    serializer_class = serializers.OutgoingSerializer

    def create(self, request, *args, **kwargs):
        outgoing_serializer = self.get_serializer(data=request.data)
        outgoing_serializer.is_valid(raise_exception=True)

        # Создаем и сохраняем объект Outgoing
        outgoing = outgoing_serializer.save()

        # Для связанных OutgoingMaterial используем вложенную сериализацию
        outgoing_material_data = request.data.get('outgoing_materials', [])
        outgoing_material_serializer = serializers.OutgoingMaterialSerializer(data=outgoing_material_data, many=True)

        if outgoing_material_serializer.is_valid():
            # Сохраняем связанные объекты OutgoingMaterial
            outgoing_material_serializer.save(outgoing=outgoing)

            # Выполняем логику обновления запасов
            for item in outgoing_material_data:
                material = item['material']
                amount = item['amount']
                warehouse = outgoing.warehouse

                if not warehouse.use_negative:
                    stock, created = Stock.objects.get_or_create(material=material, warehouse=warehouse)
                    if stock.amount < amount:
                        return Response({"message": "Negative stock is not allowed for this warehouse."},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Расходуем количество, учитывая, что отрицательный запас разрешен
                    stock, created = Stock.objects.get_or_create(material=material, warehouse=warehouse)
                    stock.amount -= amount
                    stock.save()

            headers = self.get_success_headers(outgoing_serializer.data)
            return Response(outgoing_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(outgoing_material_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------------------------------------------
