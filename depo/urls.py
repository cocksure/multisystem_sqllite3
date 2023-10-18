from django.urls import path
from depo import views

app_name = 'depo'

urlpatterns = [
    path('outgoing/', views.OutgoingListCreateView.as_view(), name='outgoing-list'),
    path('outgoing/<int:pk>/', views.OutgoingUpdateDeleteDetailView.as_view(), name='outgoing-detail'),

    path('outgoing-detail/', views.OutgoingDetailListCreateView.as_view(), name='outgoing-detail-list'),
    path('outgoing-detail/<int:pk>/', views.OutgoingDetailUpdateDeleteView.as_view(), name='outgoing-detail-detail'),

    path('incoming/', views.IncomingListCreateView.as_view(), name='incoming-list'),
    path('incoming/<int:pk>/', views.IncomingUpdateDeleteDetailView.as_view(), name='incoming-detail'),

    path('incoming-detail/', views.IncomingDetailListCreateView.as_view(), name='incoming-detail-list'),
    path('incoming-detail/<int:pk>/', views.IncomingDetailUpdateDeleteView.as_view(), name='incoming-detail-detail'),
]
