from django.db import models

from apps.depo.models.outgoing import Outgoing
from apps.depo.services import validate_incoming, process_incoming
from apps.shared.models import BaseModel


class Incoming(BaseModel):
    MOVEMENT = 'Перемешения'
    INVOICE = 'По накладной'

    INCOMING_TYPE = [
        (MOVEMENT, 'Перемешения'),
        (INVOICE, 'По накладной'),
    ]

    data = models.DateField(editable=True)
    warehouse = models.ForeignKey('info.Warehouse', on_delete=models.PROTECT, related_name='incoming_warehouse')
    from_warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='incoming_from_warehouse')
    invoice = models.CharField(max_length=150, null=True, blank=True)
    contract_number = models.CharField(max_length=150, null=True, blank=True)
    outgoing = models.ForeignKey(Outgoing, on_delete=models.PROTECT, null=True, blank=True)
    purchase = models.ForeignKey('purchase.Purchase', on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)
    incoming_type = models.CharField(choices=INCOMING_TYPE, null=True, blank=True)

    def save(self, *args, **kwargs):
        process_incoming(self)

        super().save(*args, **kwargs)

    def clean(self):
        validate_incoming(self)

        super().clean()

    def __str__(self):
        return f"{self.warehouse} {self.data}"


class IncomingMaterial(models.Model):
    incoming = models.ForeignKey(Incoming, on_delete=models.CASCADE)
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    purchase_product = models.ForeignKey('purchase.PurchaseProduct', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=150, null=True, blank=True)
    material_party = models.ForeignKey('info.MaterialParty', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.material} - {self.amount}"
