from django.db import models

from apps.shared.models import BaseModel
from apps.hr.models import Employee, Department


class PurchaseStatus(models.TextChoices):
    NEW = 'new', 'Новая'
    CONFIRMED = 'confirmed', 'Подтверждена'
    ASSIGNED = 'assigned', 'Распределена'
    REJECTED = 'rejected', 'Отклонена'
    ACCEPTED = 'accepted', 'Принята'
    DELIVERED = 'delivered', 'Доставлена'
    IN_STOCK = 'in_stock', 'В складе'


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey('purchase.Purchase', on_delete=models.PROTECT)
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    color = models.CharField(max_length=100, null=True, blank=True)
    specification = models.ForeignKey('info.Specification', on_delete=models.SET_NULL, null=True, blank=True, )
    signed_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='signed_purchaseproducts')
    signed_at = models.DateTimeField(editable=True, null=True, blank=True, )
    rejected_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='rejected_purchaseproducts')
    rejected_at = models.DateTimeField(editable=True, null=True, blank=True, )
    assigned_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_purchaseproducts_per_material')
    assigned_at = models.DateTimeField(editable=True, null=True, blank=True, )
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='executor_purchaseproducts')
    status = models.CharField(choices=PurchaseStatus.choices, default=PurchaseStatus.NEW)

    def purchase_status_validate(self):
        current_status = self.status

        if current_status == PurchaseStatus.NEW:
            if all([self.signed_by, self.signed_at]):
                self.status = PurchaseStatus.CONFIRMED
        elif current_status == PurchaseStatus.CONFIRMED:
            if all([self.rejected_by, self.rejected_at]):
                self.status = PurchaseStatus.REJECTED
            elif all([self.assigned_by, self.assigned_at]):
                self.status = PurchaseStatus.ASSIGNED

    def save(self, *args, **kwargs):
        self.purchase_status_validate()
        super().save(*args, **kwargs)
        self.purchase.update_purchase_status()

    def __str__(self):
        return str(self.id)


class Purchase(BaseModel):
    data = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE)
    requester = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    arrival_date = models.DateField(editable=True)
    status = models.CharField(choices=PurchaseStatus.choices, default=PurchaseStatus.NEW, max_length=20)
    note = models.TextField(max_length=1000, null=True, blank=True)

    def update_purchase_status(self):
        confirmed_count = self.purchaseproduct_set.filter(status=PurchaseStatus.CONFIRMED).exists()
        rejected_count = self.purchaseproduct_set.filter(status=PurchaseStatus.REJECTED).exists()
        assigned_count = self.purchaseproduct_set.filter(status=PurchaseStatus.ASSIGNED).exists()

        if confirmed_count and not rejected_count and not assigned_count:
            self.status = PurchaseStatus.CONFIRMED
        elif not confirmed_count and rejected_count and not assigned_count:
            self.status = PurchaseStatus.REJECTED
        elif not confirmed_count and not rejected_count and assigned_count:
            self.status = PurchaseStatus.ASSIGNED
        else:
            self.status = PurchaseStatus.NEW

        self.save()

    def __str__(self):
        return str(self.id)
