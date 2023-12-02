from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from rest_framework import generics, status

from hr.models import Employee
from purchase import models, serializers
from rest_framework.response import Response

from purchase.models import PurchaseProduct, Purchase, PurchaseStatus
from purchase.serializers import PurchaseProductSerializer, PurchaseSerializer
from shared.utils import CustomPagination
from shared.views import BaseListView
from shared.permissions import can_sign_purchase, can_assign_purchase


class PurchaseListView(BaseListView):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseListOnlySerializer
    filterset_fields = ['warehouse', 'department']
    search_fields = ['id', 'requester']
    pagination_class = CustomPagination


class PurchaseDetailView(generics.RetrieveAPIView):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer


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


class PurchaseConfirmationView(generics.RetrieveUpdateAPIView):
    queryset = PurchaseProduct.objects.all()
    serializer_class = PurchaseProductSerializer

    def get_purchase(self):
        purchase_id = self.kwargs.get('pk')
        return get_object_or_404(Purchase, pk=purchase_id)

    def get_material_ids(self):
        return [int(self.request.data.get('material'))]

    def get_object(self):
        purchase = self.get_purchase()
        material_ids = self.get_material_ids()

        instances = PurchaseProduct.objects.filter(purchase=purchase, material__in=material_ids).all()
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
            if instance.signed_by or instance.rejected_by:
                return Response({"detail": "Material already signed or rejected."}, status=status.HTTP_400_BAD_REQUEST)

            if action == 'accept':
                instance.signed_by = request.user if request.user.is_authenticated else None
                instance.signed_at = timezone.now()
            elif action == 'reject':
                instance.rejected_by = request.user if request.user.is_authenticated else None
                instance.rejected_at = timezone.now()

            instance.save()
            instance.purchase.update_purchase_status()

        serializer = PurchaseProductSerializer(instances, many=True)
        return Response(serializer.data)


class ConfirmedPurchaseListView(generics.ListAPIView):
    queryset = models.Purchase.objects.filter(status='confirmed')
    serializer_class = serializers.PurchaseListOnlySerializer
    filterset_fields = ['warehouse', 'department']
    search_fields = ['id', 'requester']
    pagination_class = CustomPagination


class AssignPurchaseView(generics.UpdateAPIView):
    queryset = PurchaseProduct.objects.all()
    serializer_class = PurchaseProductSerializer

    def get_purchase(self):
        purchase_id = self.kwargs.get('pk')
        return get_object_or_404(Purchase, pk=purchase_id)

    def get_object(self):
        purchase = self.get_purchase()

        purchase_products = PurchaseProduct.objects.filter(
            purchase=purchase,
        )

        return purchase_products

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        purchase_products_data = request.data

        if not purchase_products_data:
            return Response({"detail": "No data provided for distribution."},
                            status=status.HTTP_400_BAD_REQUEST)

        purchase_products = [get_object_or_404(PurchaseProduct, pk=item.get('purchase_product_id'))
                             for item in purchase_products_data]

        for purchase_product_data, purchase_product in zip(purchase_products_data, purchase_products):
            assigned_to_id = purchase_product_data.get('assigned_to', None)

            if not can_assign_purchase(request.user):
                return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

            if assigned_to_id is not None:
                if purchase_product.status in [PurchaseStatus.CONFIRMED]:
                    assigned_to = get_object_or_404(Employee, pk=assigned_to_id, department__id=2)
                    purchase_product.assigned_by = request.user
                    purchase_product.assigned_to = assigned_to
                    purchase_product.assigned_at = timezone.now()
                    try:
                        purchase_product.save()
                    except Exception as e:
                        return Response({"detail": f"Failed to save purchase product. {str(e)}"},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response(
                        {"detail": "Cannot reassign product with status other than 'confirmed"},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "assigned_to field is required for distribution."},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Distribution successful."}, status=status.HTTP_200_OK)


class AssignedPurchaseListView(generics.ListAPIView):
    queryset = models.Purchase.objects.filter(status='assigned')
    serializer_class = serializers.PurchaseSerializer
    pagination_class = CustomPagination
