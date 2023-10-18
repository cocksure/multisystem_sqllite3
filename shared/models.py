from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True,
                                   related_name='%(class)s_created_by')
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True,
                                   related_name='%(class)s_updated_by')
    created_time = models.DateTimeField(default=timezone.now, editable=True)
    updated_time = models.DateTimeField(default=timezone.now, editable=True)

    class Meta:
        ordering = ['-created_time']
        abstract = True


class BaseDetail(BaseModel):
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=150, null=True, blank=True)
    material_party = models.CharField(max_length=100, null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        abstract = True
