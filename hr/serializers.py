from rest_framework.serializers import ModelSerializer
from hr import models


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'


class PositionSerializer(ModelSerializer):
    class Meta:
        model = models.Position
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'
