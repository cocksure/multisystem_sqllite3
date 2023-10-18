from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from hr import serializers, models
from shared.views import BaseListView


class DepartmentListCreateView(BaseListView):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class PositionListCreateView(BaseListView):
    queryset = models.Position.objects.all()
    serializer_class = serializers.PositionSerializer


class EmployeeListCreateView(BaseListView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class DepartmentDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class PositionDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Position.objects.all()
    serializer_class = serializers.PositionSerializer


class EmployeeDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
