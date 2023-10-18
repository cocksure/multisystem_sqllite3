from django.urls import path
from . import views

urlpatterns = [
    path('purchases/', views.PurchaseListCreateView.as_view(), name='purchase-list'),
    path('purchases/<int:pk>/', views.PurchaseDetailUpdateDeleteView.as_view(), name='purchase-detail'),

    path('purchase-products/', views.PurchaseProductListCreateView.as_view(), name='purchase-product-list'),
    path('purchase-products/<int:pk>/', views.PurchaseProductUpdateDeleteView.as_view(),
         name='purchase-product-detail'),
]
