from django.urls import path
from info.views import material, warehouse, infos

app_name = 'info'

urlpatterns = [
    path('materials/', material.MaterialListCreateView.as_view(), name='material-list'),
    path('materials/<int:pk>/', material.MaterialDetailUpdateDeleteView.as_view(), name='material-detail'),

    path('specs/', infos.SpecListCreateView.as_view(), name='spec-list'),
    path('specs/<int:pk>/', infos.SpecDetailUpdateDeleteView.as_view(), name='spec-detail'),

    path('units/', infos.UnitListCreateView.as_view(), name='unit-list'),
    path('units/<int:pk>/', infos.UnitDetailUpdateDeleteView.as_view(), name='unit-detail'),

    path('firms/', infos.FirmListCreateView.as_view(), name='firm-list'),
    path('firms/<int:pk>/', infos.FirmDetailUpdateDeleteView.as_view(), name='firm-detail'),

    path('material-groups/', material.MaterialGroupListCreateView.as_view(), name='material-group-list'),
    path('material-groups/<int:pk>/', material.MaterialGroupDetailUpdateDeleteView.as_view(),
         name='material-group-detail'),

    path('material-types/', material.MaterialTypeListCreateView.as_view(), name='material-type-list'),
    path('material-types/<int:pk>/', material.MaterialTypeDetailUpdateDeleteView.as_view(), name='material-type-detail'),

    path('warehouses/', warehouse.WarehouseListCreateView.as_view(), name='warehouse-list'),
    path('warehouses/<int:pk>/', warehouse.WarehouseDetailUpdateDeleteView.as_view(), name='warehouse-detail'),

    path('devices/', infos.DeviceListCreateView.as_view(), name='device-list'),
    path('devices/<int:pk>/', infos.DeviceDetailUpdateDeleteView.as_view(), name='device-detail'),

    path('currencies/', infos.CurrencyListCreateView.as_view(), name='currency-list'),
    path('currencies/<int:pk>/', infos.CurrencyDetailUpdateDeleteView.as_view(), name='currency-detail'),

    path('dealers/', infos.DealerListCreateView.as_view(), name='dealer-list'),
    path('dealers/<int:pk>/', infos.DealerDetailUpdateDeleteView.as_view(), name='dealer-detail'),

    path('brands/', infos.BrandListCreateView.as_view(), name='brand-list'),
    path('brands/<int:pk>/', infos.BrandDetailUpdateDeleteView.as_view(), name='brand-detail'),
]
