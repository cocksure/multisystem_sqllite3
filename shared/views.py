from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


class BaseListView(generics.ListCreateAPIView):
    queryset = None
    serializer_class = None
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save()

    def get(self, request, *args, **kwargs):
        page_size = request.query_params.get('page_size', None)
        if page_size:
            self.pagination_class.page_size = page_size
        return self.list(request, *args, **kwargs)
