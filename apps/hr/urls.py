from django.urls import path
from . import views

app_name = 'hr'


urlpatterns = [
    path('divisions/', views.DivisionsListCreateView.as_view(), name='division-list'),

    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list'),

    path('positions/', views.PositionListCreateView.as_view(), name='position-list'),

    path('employees/', views.EmployeeListCreateView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', views.EmployeeDetailUpdateDeleteView.as_view(), name='employee-detail'),

    path('employee/export/<int:pk>/', views.EmployeePDFExportView.as_view(), name='employee_export'),

]
