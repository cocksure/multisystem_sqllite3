from rest_framework import generics, status
from rest_framework.response import Response

from depo import serializers, models
from shared.views import BaseListView


class IncomingListCreateView(BaseListView):
    queryset = models.Incoming.objects.all()
    serializer_class = serializers.IncomingSerializer
    filterset_fields = ['warehouse']
    search_fields = ['code']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        details_data = request.data.get('incomingdetail_set')
        if details_data:
            for detail_data in details_data:
                detail_data['incoming'] = serializer.instance.pk
            detail_serializer = serializers.IncomingDetailSerializer(data=details_data, many=True)
            detail_serializer.is_valid(raise_exception=True)
            detail_serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class IncomingDetailListCreateView(BaseListView):
    queryset = models.IncomingDetail.objects.all()
    serializer_class = serializers.IncomingDetailSerializer


class IncomingUpdateDeleteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Incoming.objects.all()
    serializer_class = serializers.IncomingSerializer


class IncomingDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.IncomingDetail.objects.all()
    serializer_class = serializers.IncomingDetailSerializer
