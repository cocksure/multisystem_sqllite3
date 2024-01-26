from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('', views.PurchaseListView.as_view(), name='purchase-list'),
    path('create/', views.PurchaseCreateView.as_view(), name='purchase-create'),
    path('<int:pk>/', views.PurchaseDetailView.as_view(), name='purchase-detail'),
    path('confirm/<int:pk>/', views.PurchaseConfirmationView.as_view(), name='purchase-confirm'),
    path('confirmed/', views.ConfirmedPurchaseListView.as_view(), name='confirmed-purchase-list'),
    path('assign/<int:pk>/', views.AssignPurchaseView.as_view(), name='assign-purchase'),
    path('assigns/', views.AssignedPurchaseListView.as_view(), name='assigned-list'),

]
