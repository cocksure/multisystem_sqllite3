from rest_framework import serializers
from apps.users import models


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)
