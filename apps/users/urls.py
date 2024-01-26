from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.UsersListView.as_view(), name='employee-list'),
]
