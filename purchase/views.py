from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone
from rest_framework import generics, status
from purchase import models, serializers
from rest_framework.response import Response

from shared.views import BaseListView
from shared.permissions import can_sign_purchase


class PurchaseListView(BaseListView):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer
    filterset_fields = ['warehouse', 'department']
    search_fields = ['id', 'requester']


class PurchaseCreateView(generics.CreateAPIView):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        purchase_data = request.data.copy()
        purchase_product_data = purchase_data.pop('purchase_products', [])

        purchase_data['created_by'] = request.user.id if request.user.is_authenticated else None
        purchase_data['data'] = timezone.now()

        purchase_serializer = self.get_serializer(data=purchase_data)
        purchase_serializer.is_valid(raise_exception=True)

        purchase = purchase_serializer.save()

        purchase_product_data = [{'purchase': purchase.id, **item} for item in purchase_product_data]
        purchase_product_serializer = serializers.PurchaseProductSerializer(data=purchase_product_data, many=True)

        if purchase_product_serializer.is_valid():
            purchase_product_serializer.save()

            try:
                purchase.full_clean()
            except ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            headers = self.get_success_headers(purchase_serializer.data)
            return Response(purchase_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(purchase_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseDetailView(generics.RetrieveAPIView):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer


class PurchaseConfirmationView(generics.RetrieveUpdateAPIView):
    queryset = models.PurchaseProduct.objects.all()
    serializer_class = serializers.PurchaseProductSerializer

    def get_object(self):
        purchase_id = self.kwargs.get('pk')
        material_ids = [action.get('material') for action in self.request.data]

        instances = get_list_or_404(models.PurchaseProduct, purchase=purchase_id, material__in=material_ids)
        return instances

    def update(self, request, *args, **kwargs):
        instances = self.get_object()

        if not instances:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if not can_sign_purchase(request.user):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        action = request.data.get('action', None)

        if action not in ['accept', 'reject']:
            return Response({"detail": "Invalid action parameter."}, status=status.HTTP_400_BAD_REQUEST)

        for instance in instances:
            if action == 'accept':
                instance.accepted_by = request.user if request.user.is_authenticated else None
                instance.accepted_at = timezone.now()
            elif action == 'reject':
                instance.rejected_by = request.user if request.user.is_authenticated else None
                instance.rejected_at = timezone.now()

            instance.save()

            # Важно: каждый объект PurchaseProduct обрабатывается отдельно
            instance.purchase.update_purchase_status()

        # Возвращаем сериализованные данные для всех объектов
        serializer = serializers.PurchaseProductSerializer(instances, many=True)
        return Response(serializer.data)


class PurchaseDistributionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.distributed_at = timezone.now()
        instance.distributed_to = request.user if request.user.is_authenticated else None
        instance.save()
        return Response(serializers.PurchaseSerializer(instance).data)
