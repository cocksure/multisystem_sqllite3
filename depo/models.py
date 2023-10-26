from django.core.exceptions import ValidationError
from django.db import models
from shared.models import BaseModel
from django.db.models.signals import pre_save


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

    def clean(self):
        if self.type == self.MOVEMENT:
            if not self.to_warehouse:
                raise ValidationError('Выберите склад в поле "to_warehouse", так как тип - перемещения.')
            if self.to_warehouse == self.warehouse:
                raise ValidationError('Нельзя перемещать товары на тот же самый склад.')

    def __str__(self):
        return self.code


def generate_outgoing_code(sender, instance, **kwargs):
    if not instance.code:
        last_outgoing = Outgoing.objects.order_by('-id').first()
        if last_outgoing:
            last_id = last_outgoing.id
            new_id = int(last_id) + 1
            instance.code = f'WA{str(new_id).zfill(6)}'
        else:
            instance.code = 'WA000001'


pre_save.connect(generate_outgoing_code, sender=Outgoing)


class Incoming(BaseModel):
    data = models.DateField(auto_now_add=True)
    warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE, related_name='incoming_warehouse')
    from_warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='incoming_from_warehouse')
    invoice = models.CharField(max_length=150, null=True, blank=True)
    contract_number = models.CharField(max_length=150, null=True, blank=True)
    outgoing = models.ForeignKey(Outgoing, on_delete=models.CASCADE, null=True, blank=True)
    purchase = models.ForeignKey('purchase.Purchase', on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.warehouse} {self.data}"


class IncomingDetail(models.Model):
    incoming = models.ForeignKey(Incoming, on_delete=models.CASCADE)
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    purchase_product = models.ForeignKey('purchase.PurchaseProduct', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=150, null=True, blank=True)
    material_party = models.ForeignKey('info.MaterialParty', on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.material} - {self.amount}"


class OutgoingDetail(models.Model):
    outgoing = models.ForeignKey(Outgoing, on_delete=models.CASCADE)
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=150, null=True, blank=True)
    material_party = models.ForeignKey('info.MaterialParty', on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, null=True, blank=True)


class Stock(models.Model):
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.material} в {self.warehouse} ({self.quantity} шт.)"
