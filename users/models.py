from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='users_photos', default='default-profile__picture.jpg', null=True,
                                      blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg',
                                                                                                         'png', 'heir',
                                                                                                         'heif'])])

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()
