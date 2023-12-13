from django.db import models


class BaseModel(models.Model):
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True,
                                   related_name='%(class)s_created_by')
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL,
                                   related_name='%(class)s_updated_by', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, editable=True, blank=True, null=True)
    updated_time = models.DateTimeField(auto_now=True, editable=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.updated_by and hasattr(self, 'request') and getattr(self, 'request'):
            self.updated_by = self.request.user

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']
        abstract = True


class MainMenu(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class SubMenu(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    parent = models.ForeignKey(MainMenu, on_delete=models.CASCADE, related_name='submenus')

    def __str__(self):
        return self.title