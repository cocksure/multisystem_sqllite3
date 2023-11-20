from django.db import models


class Stock(models.Model):
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    material_party = models.ForeignKey('info.MaterialParty', on_delete=models.CASCADE, null=True, blank=True)
    warehouse = models.ForeignKey('info.Warehouse', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.material and not self.material_party:
            self.material_party = self.material.material_party

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.material} в {self.warehouse} ({self.amount} шт.)"
