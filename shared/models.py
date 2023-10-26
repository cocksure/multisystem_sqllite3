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
