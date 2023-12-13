from rest_framework import serializers

from shared.models import SubMenu, MainMenu


class BaseNameCodeSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True

    def validate(self, data):
        code = data.get('code')
        name = data.get('name')

        if code and name and code == name:
            raise serializers.ValidationError('Код и имя не должны быть одинаковыми.')

        if name.isnumeric():
            raise serializers.ValidationError("Имя не должно содержать только цифры.")

        return data


class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields = ['id', 'title', 'url', 'parent']


class MainMenuSerializer(serializers.ModelSerializer):
    submenus = SubMenuSerializer(many=True, read_only=True)

    class Meta:
        model = MainMenu
        fields = ['id', 'title', 'submenus']
