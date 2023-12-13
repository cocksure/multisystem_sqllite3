from rest_framework import generics

from shared.models import MainMenu, SubMenu
from shared.serializers import MainMenuSerializer, SubMenuSerializer
from shared.utils import CustomPagination


class BaseListView(generics.ListAPIView):
    queryset = None
    serializer_class = None
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save()

    def get(self, request, *args, **kwargs):
        page_size = request.query_params.get('page_size', None)
        if page_size:
            self.pagination_class.page_size = page_size
        return self.list(request, *args, **kwargs)


class MainMenuListCreateView(generics.ListCreateAPIView):
    queryset = MainMenu.objects.all()
    serializer_class = MainMenuSerializer


class SubMenuListCreateView(generics.ListCreateAPIView):
    queryset = SubMenu.objects.all()
    serializer_class = SubMenuSerializer
