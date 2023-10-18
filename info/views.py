from rest_framework import generics
from info import models, serializers
from shared.views import BaseListView


class SpecListCreateView(BaseListView):
    queryset = models.Specification.objects.all()
    serializer_class = serializers.SpecSerializer


class UnitListCreateView(BaseListView):
    queryset = models.Unit.objects.all()
    serializer_class = serializers.UnitSerializer


class FirmListCreateView(BaseListView):
    queryset = models.Firm.objects.all()
    serializer_class = serializers.FirmSerializer


class MaterialGroupListCreateView(BaseListView):
    queryset = models.MaterialGroup.objects.all()
    serializer_class = serializers.MaterialGroupSerializer


class MaterialTypeListCreateView(BaseListView):
    queryset = models.MaterialType.objects.all()
    serializer_class = serializers.MaterialTypeSerializer


class WarehouseListCreateView(BaseListView):
    queryset = models.Warehouse.objects.all()
    serializer_class = serializers.WarehouseSerializer


class DeviceListCreateView(BaseListView):
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer


class CurrencyListCreateView(BaseListView):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer


class DealerListCreateView(BaseListView):
    queryset = models.Dealer.objects.all()
    serializer_class = serializers.DealerSerializer


class BrandListCreateView(BaseListView):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer


class MaterialListCreateView(BaseListView):
    queryset = models.Material.objects.all()
    serializer_class = serializers.MaterialSerializer


class SpecDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Specification.objects.all()
    serializer_class = serializers.SpecSerializer


class UnitDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Unit.objects.all()
    serializer_class = serializers.UnitSerializer


class FirmDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Firm.objects.all()
    serializer_class = serializers.FirmSerializer


class MaterialGroupDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MaterialGroup.objects.all()
    serializer_class = serializers.MaterialGroupSerializer


class MaterialTypeDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MaterialType.objects.all()
    serializer_class = serializers.MaterialTypeSerializer


class WarehouseDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Warehouse.objects.all()
    serializer_class = serializers.WarehouseSerializer


class DeviceDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer


class CurrencyDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer


class DealerDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Dealer.objects.all()
    serializer_class = serializers.DealerSerializer


class BrandDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer


class MaterialDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Material.objects.all()
    serializer_class = serializers.MaterialSerializer
