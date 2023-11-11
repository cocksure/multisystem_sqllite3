from django.urls import path
from depo.views import incoming, outgoing, stock

app_name = 'depo'

urlpatterns = [
    path('incoming/', incoming.IncomingListView.as_view(), name='incoming-list'),
    path('incoming/create', incoming.IncomingCreateView.as_view(), name='incoming-create'),

    path('outgoing/', outgoing.OutgoingListView.as_view(), name='outgoing-list'),
    path('outgoing/create', outgoing.OutgoingCreateView.as_view(), name='outgoing-create'),
    path('outgoing/detail/<int:pk>/', outgoing.OutgoingDetailView.as_view(), name='outgoing-detail'),

    path('stock/', stock.StockListView.as_view(), name='stock-list'),
    path('stock-detail/<int:pk>/', stock.StockDetailView.as_view(), name='stock-detail'),
]
