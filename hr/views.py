from rest_framework import generics

from hr import serializers, models
from shared.views import BaseListView


class DivisionsListCreateView(BaseListView):
    queryset = models.Division.objects.all()
    serializer_class = serializers.DivisionSerializer
    search_fields = ['name']


class DepartmentListCreateView(BaseListView):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    filterset_fields = ['divisions']
    search_fields = ['name', ]


class PositionListCreateView(BaseListView):
    queryset = models.Position.objects.all()
    serializer_class = serializers.PositionSerializer

    search_fields = ['name', ]


class EmployeeListCreateView(BaseListView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    filterset_fields = ['gender', 'department', 'position', 'is_fired']
    search_fields = ['full_name', '=report_card', '=badge_number', '=passport_pin']


class DivisionDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Division.objects.all()
    serializer_class = serializers.DivisionSerializer


class DepartmentDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class PositionDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Position.objects.all()
    serializer_class = serializers.PositionSerializer


class EmployeeDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
