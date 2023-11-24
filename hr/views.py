from rest_framework import generics

from hr import serializers, models
from shared.views import BaseListView


# ------------------------------Employee-------------------------------------
class EmployeeListCreateView(generics.ListCreateAPIView, BaseListView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    filterset_fields = ['gender', 'department', 'position', 'is_fired']
    search_fields = ['full_name', '=report_card', '=badge_number', '=passport_pin']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EmployeeDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


# ------------------------------Employee----------------------------------------------

class DivisionsListCreateView(generics.ListCreateAPIView):
    queryset = models.Division.objects.all()
    serializer_class = serializers.DivisionSerializer
    search_fields = ['name']


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    filterset_fields = ['divisions']
    search_fields = ['name', ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PositionListCreateView(generics.ListCreateAPIView):
    queryset = models.Position.objects.all()
    serializer_class = serializers.PositionSerializer

    search_fields = ['name', ]
