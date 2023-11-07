from django.urls import path
from depo.views import incoming, outgoing, stock


app_name = 'depo'

urlpatterns = [
    path('outgoing/', outgoing.OutgoingListCreateView.as_view(), name='outgoing-list'),

    path('outgoing-detail/', outgoing.OutgoingDetailListCreateView.as_view(), name='outgoing-detail-list'),

    path('incoming/', incoming.IncomingListCreateView.as_view(), name='incoming-list'),

    path('incoming-detail/', incoming.IncomingDetailListCreateView.as_view(), name='incoming-detail-list'),

    path('stock/', stock.StockListView.as_view(), name='stock-list'),
    path('stock-detail/<int:pk>/', stock.StockDetailView.as_view(), name='stock-detail'),
]
