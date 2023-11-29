from depo.services import validate_outgoing, validate_use_negative, validate_movement_outgoing
from shared.models import BaseModel
from django.db import models


# -------------------------------------------------------------------------------------
class Outgoing(BaseModel):
    class OutgoingType(models.TextChoices):
        OUTGO = 'расход', 'Расход'
        SALE = 'продажа', 'Продажа'
        MOVEMENT = 'перемешения', 'Перемещение'

    class OutgoingStatus(models.TextChoices):
        ACCEPT = 'Принят', 'Принят'
        REJECT = 'Отклонен', 'Отклонен'
        IN_PROGRESS = 'В ожидании', 'В ожидании'

    code = models.CharField(max_length=10, unique=True, editable=False)
    data = models.DateField(editable=True)
    outgoing_type = models.CharField(max_length=20, choices=OutgoingType.choices, default=OutgoingType.MOVEMENT)

    warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE, related_name='outgoing_warehouse')
    to_warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='outgoing_to_warehouse')
    status = models.CharField(max_length=20, choices=OutgoingStatus.choices, default=OutgoingStatus.IN_PROGRESS,
                              null=True, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)

    id = models.AutoField(primary_key=True)

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
        validate_movement_outgoing(self)
        validate_use_negative(self, self.outgoing_materials)
        super().clean()

    def __str__(self):
        return self.code


# -------------------------------------------------------------------------------------


class OutgoingMaterial(models.Model):
    outgoing = models.ForeignKey(Outgoing, on_delete=models.CASCADE, related_name='outgoing_materials')
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=150, null=True, blank=True)
    material_party = models.ForeignKey('info.MaterialParty', on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.material} {self.amount}"
