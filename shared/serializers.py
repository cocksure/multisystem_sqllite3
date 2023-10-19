from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class BaseNameCodeSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True

    def validate(self, data):
        code = data.get('code')
        name = data.get('name')

        if code and name and code == name:
            raise ValidationError('Код и имя не должны быть одинаковыми.')

        return data
