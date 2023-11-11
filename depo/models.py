from django.db import models

from info.models import Material
from shared.models import BaseModel
from .services import validate_movement_outgoing, process_incoming, validate_outgoing, validate_incoming


class Outgoing(BaseModel):
    OUTGO, SALE, MOVEMENT = ('расход', 'продажа', 'перемешения')

    OUTGOING_TYPE = (
        (OUTGO, OUTGO),
        (SALE, SALE),
        (MOVEMENT, MOVEMENT)
    )
    code = models.CharField(max_length=10, unique=True, editable=False)
    data = models.DateField(editable=True)
    type = models.CharField(choices=OUTGOING_TYPE, default=MOVEMENT)

    warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE, related_name='outgoing_warehouse')
    to_warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='outgoing_to_warehouse')
    note = models.CharField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_outgoing = Outgoing.objects.order_by('-id').first()
            if last_outgoing:
                last_id = last_outgoing.id
                new_id = int(last_id) + 1
                self.code = f'WA{str(new_id).zfill(6)}'
            else:
                self.code = 'WA000001'

        super().save(*args, **kwargs)

    def clean(self):
        validate_outgoing(self)

        if self.type == self.MOVEMENT:
            validate_movement_outgoing(self)

        super().clean()

    def __str__(self):
        return self.code


class Incoming(BaseModel):
    ACCEPT, REJECT, IN_PROGRESS = ('Принят', 'Отклонен', 'В ожидании')

    INCOMING_STATUS = (
        (ACCEPT, ACCEPT),
        (REJECT, REJECT),
        (IN_PROGRESS, IN_PROGRESS)
    )

    MOVEMENT, INVOICE = ('Перемешения', 'По накладной')

    INCOMING_TYPE = (
        (MOVEMENT, MOVEMENT),
        (INVOICE, INVOICE)
    )

    data = models.DateField(auto_now_add=True)
    warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE, related_name='incoming_warehouse')
    from_warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='incoming_from_warehouse')
    invoice = models.CharField(max_length=150, null=True, blank=True)
    contract_number = models.CharField(max_length=150, null=True, blank=True)
    outgoing = models.ForeignKey(Outgoing, on_delete=models.CASCADE, null=True, blank=True)
    purchase = models.ForeignKey('purchase.Purchase', on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(choices=INCOMING_STATUS, default=None, null=True, blank=True)
    type = models.CharField(choices=INCOMING_TYPE, null=True, blank=True)

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
    material_party = models.ForeignKey('info.MaterialParty', on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.material} - {self.amount}"


class OutgoingMaterial(models.Model):
    outgoing = models.ForeignKey(Outgoing, on_delete=models.CASCADE)
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=150, null=True, blank=True)
    material_party = models.ForeignKey('info.MaterialParty', on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, null=True, blank=True)


class Stock(models.Model):
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)

    def spend(self, amount, use_negative=False):
        if use_negative or self.amount >= amount:
            self.amount -= amount
            self.save()
            return True
        else:
            return False

    def __str__(self):
        return f"{self.material} в {self.warehouse} ({self.amount} шт.)"
