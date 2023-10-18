from django.core.exceptions import ValidationError
from django.db import models
from info.models import Warehouse
from shared.models import BaseModel, BaseDetail
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

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='outgoing_warehouse')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True,
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
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='incoming_warehouse')
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='incoming_from_warehouse')
    invoice = models.CharField(max_length=150, null=True, blank=True)
    contract_number = models.CharField(max_length=150, null=True, blank=True)
    outgoing = models.ForeignKey(Outgoing, on_delete=models.CASCADE, null=True, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)


class IncomingDetail(BaseDetail):
    incoming = models.ForeignKey(Incoming, on_delete=models.CASCADE)


class DetailOutgoing(BaseDetail):
    outgoing = models.ForeignKey(Outgoing, on_delete=models.CASCADE)
