from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('materials/', views.MaterialListCreateView.as_view(), name='material-list'),
    path('materials/<int:pk>/', views.MaterialDetailUpdateDeleteView.as_view(), name='material-detail'),

    path('specs/', views.SpecListCreateView.as_view(), name='spec-list'),
    path('specs/<int:pk>/', views.SpecDetailUpdateDeleteView.as_view(), name='spec-detail'),

    path('units/', views.UnitListCreateView.as_view(), name='unit-list'),
    path('units/<int:pk>/', views.UnitDetailUpdateDeleteView.as_view(), name='unit-detail'),

    path('firms/', views.FirmListCreateView.as_view(), name='firm-list'),
    path('firms/<int:pk>/', views.FirmDetailUpdateDeleteView.as_view(), name='firm-detail'),

    path('material-groups/', views.MaterialGroupListCreateView.as_view(), name='material-group-list'),
    path('material-groups/<int:pk>/', views.MaterialGroupDetailUpdateDeleteView.as_view(),
         name='material-group-detail'),

    path('material-types/', views.MaterialTypeListCreateView.as_view(), name='material-type-list'),
    path('material-types/<int:pk>/', views.MaterialTypeDetailUpdateDeleteView.as_view(), name='material-type-detail'),

    path('warehouses/', views.WarehouseListCreateView.as_view(), name='warehouse-list'),
    path('warehouses/<int:pk>/', views.WarehouseDetailUpdateDeleteView.as_view(), name='warehouse-detail'),

    path('devices/', views.DeviceListCreateView.as_view(), name='device-list'),
    path('devices/<int:pk>/', views.DeviceDetailUpdateDeleteView.as_view(), name='device-detail'),

    path('currencies/', views.CurrencyListCreateView.as_view(), name='currency-list'),
    path('currencies/<int:pk>/', views.CurrencyDetailUpdateDeleteView.as_view(), name='currency-detail'),

    path('dealers/', views.DealerListCreateView.as_view(), name='dealer-list'),
    path('dealers/<int:pk>/', views.DealerDetailUpdateDeleteView.as_view(), name='dealer-detail'),

    path('brands/', views.BrandListCreateView.as_view(), name='brand-list'),
    path('brands/<int:pk>/', views.BrandDetailUpdateDeleteView.as_view(), name='brand-detail'),
]
