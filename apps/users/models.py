from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class CustomUser(AbstractUser, PermissionsMixin):
    can_sign_purchase = models.BooleanField(default=False)
    can_assign_purchase = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if not self.employee or self.employee.is_fired:
    #         self.is_active = False
    #     super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()
