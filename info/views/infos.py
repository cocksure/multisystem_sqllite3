from rest_framework import viewsets
from shared.utils import CustomPagination

from info.serializers import infos
from info import models


class SpecificationViewSetView(viewsets.ModelViewSet):
    queryset = models.Specification.objects.all()
    serializer_class = infos.SpecSerializer
    search_fields = ['name']
    pagination_class = CustomPagination


class UnitViewSetView(viewsets.ModelViewSet):
    queryset = models.Unit.objects.all().order_by('id')
    serializer_class = infos.UnitSerializer
    search_fields = ['code', 'name']
    pagination_class = CustomPagination


class FirmViewSetView(viewsets.ModelViewSet):
    queryset = models.Firm.objects.all()
    serializer_class = infos.FirmSerializer
    filterset_fields = ['type']
    search_fields = ['code', 'name']
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(udated_by=self.request.user)


class DeviceViewSetView(viewsets.ModelViewSet):
    queryset = models.Device.objects.all()
    serializer_class = infos.DeviceSerializer
    search_fields = ['code', 'name']
    pagination_class = CustomPagination


class CurrencyViewSetView(viewsets.ModelViewSet):
    queryset = models.Currency.objects.all()
    serializer_class = infos.CurrencySerializer
    search_fields = ['code', 'name']
    pagination_class = CustomPagination


class DealerViewSetView(viewsets.ModelViewSet):
    queryset = models.Dealer.objects.all()
    serializer_class = infos.DealerSerializer
    search_fields = ['name']
    pagination_class = CustomPagination


class BrandViewSetView(viewsets.ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = infos.BrandSerializer
    search_fields = ['name']
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)