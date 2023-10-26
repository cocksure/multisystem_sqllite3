from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from hr import models


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = models.Department
        fields = ('id', 'name', 'amount_of_employee' )

    def validate(self, attrs):
        name = attrs.get('name')

        if name.exist():
            raise serializers.ValidationError("Такой отдел ужу есть")



class PositionSerializer(ModelSerializer):
    class Meta:
        model = models.Position
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'

    def validate(self, data):
        full_name = data.get('full_name', '')

        if not all(char.isalpha() or char.isspace() for char in full_name):
            raise serializers.ValidationError({
                "status": False,
                "message": "ФИО должен содержать только буквы, пробелы и дефисы."
            })

        return data

    def validate_phone_number(self, value):
        cleaned_value = ''.join(char for char in value if char.isdigit() or char in ['+'])

        if len(cleaned_value) < 9:
            raise serializers.ValidationError("Номер телефона слишком короткий.")

        return cleaned_value
