from django.db import models

from shared.models import BaseModel

PURCHASE_STATUS = (
    ('new', 'Новая'),
    ('confirmed', 'Подтверждена'),
    ('distributed', 'Распределена'),
    ('rejected', 'Отклонена'),
    ('accepted', 'Принята'),
    ('delivered', 'Доставлена'),
    ('in_stock', 'В складе')
)


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey('purchase.Purchase', on_delete=models.CASCADE)
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
    distributed_at = models.DateTimeField(editable=True, null=True, blank=True, )
    accepted_at = models.DateTimeField(editable=True, null=True, blank=True, )
    status = models.CharField(choices=PURCHASE_STATUS, default='new')

    def purchase_status_validate(self):
        if self.signed_by and self.signed_at:
            self.status = 'confirmed'
        if self.rejected_by and self.rejected_at:
            self.status = 'rejected'

    def save(self, *args, **kwargs):
        self.purchase_status_validate()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class Purchase(BaseModel):
    data = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey('hr.Department', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE)
    requester = models.ForeignKey('hr.Employee', on_delete=models.SET_NULL, null=True)
    arrival_date = models.DateField(editable=True)
    status = models.CharField(choices=PURCHASE_STATUS, default='new')
    note = models.TextField(max_length=1000, null=True, blank=True)

    def update_purchase_status(self):
        purchase_products = models.PurchaseProduct.objects.filter(purchase=self)

        if all(product.status == 'accepted' for product in purchase_products):
            self.status = 'confirmed'
        elif any(product.status == 'rejected' for product in purchase_products):
            self.status = 'rejected'
        else:
            self.status = 'new'

        self.save()

    def __str__(self):
        return str(self.id)
