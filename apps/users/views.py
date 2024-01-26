from apps.shared.views import BaseListView
from apps.users import serializers
from apps.users import models


class UsersListView(BaseListView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer
