from django.urls import path
from depo.views import incoming, outgoing, stock


app_name = 'depo'

urlpatterns = [
    path('outgoing/', outgoing.OutgoingListCreateView.as_view(), name='outgoing-list'),
    path('outgoing/<int:pk>/', outgoing.OutgoingUpdateDeleteDetailView.as_view(), name='outgoing-detail'),

    path('outgoing-detail/', outgoing.OutgoingDetailListCreateView.as_view(), name='outgoing-detail-list'),
    path('outgoing-detail/<int:pk>/', outgoing.OutgoingDetailUpdateDeleteView.as_view(), name='outgoing-detail-detail'),

    path('incoming/', incoming.IncomingListCreateView.as_view(), name='incoming-list'),
    path('incoming/<int:pk>/', incoming.IncomingUpdateDeleteDetailView.as_view(), name='incoming-detail'),

    path('incoming-detail/', incoming.IncomingDetailListCreateView.as_view(), name='incoming-detail-list'),
    path('incoming-detail/<int:pk>/', incoming.IncomingDetailUpdateDeleteView.as_view(), name='incoming-detail-detail'),

    path('stock/', stock.StockListView.as_view(), name='stock-list'),
    path('stock-detail/<int:pk>/', stock.StockDetailView.as_view(), name='stock-detail'),
]
