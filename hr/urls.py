from django.urls import path
from . import views

app_name = 'hr'


urlpatterns = [
    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list'),
    path('departments/<int:pk>/', views.DepartmentDetailUpdateDelete.as_view(), name='department-detail'),

    path('positions/', views.PositionListCreateView.as_view(), name='position-list'),
    path('positions/<int:pk>/', views.PositionDetailUpdateDeleteView.as_view(), name='position-detail'),

    path('employees/', views.EmployeeListCreateView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', views.EmployeeDetailUpdateDeleteView.as_view(), name='employee-detail'),
]
