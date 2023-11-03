from django.core import validators
from django.db import models
from shared.validators import code_name_validate

from shared.models import BaseModel


class Unit(models.Model):
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        code_name_validate(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# should do
class Specification(models.Model):
    pass


class Firm(BaseModel):
    CUSTOMER, PROVIDER, CUSTOMER_SUPPLIER = ('Заказчик', 'Поставщик', 'Заказчик-поставщик')

    FIRM_TYPE = (
        (CUSTOMER, CUSTOMER),
        (PROVIDER, PROVIDER),
        (CUSTOMER_SUPPLIER, CUSTOMER_SUPPLIER)
    )

    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=FIRM_TYPE, default=CUSTOMER)
    legal_address = models.CharField(max_length=150, null=True, blank=True)
    actual_address = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    fax_machine = models.CharField(max_length=20, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    agent = models.ForeignKey('hr.Employee', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        code_name_validate(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MaterialGroup(models.Model):
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        code_name_validate(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MaterialType(models.Model):
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        code_name_validate(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MaterialParty(BaseModel):
    material = models.ForeignKey('info.Material', on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return self.code


class Material(BaseModel):
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    group = models.ForeignKey(MaterialGroup, on_delete=models.CASCADE)
    type = models.ForeignKey(MaterialType, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    color = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='materials_photos', default='material_default_picture.png', null=True,
                              blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    note = models.TextField(max_length=1000, null=True, blank=True)
    warranty = models.DurationField(null=True, blank=True)
    size_and_shape = models.CharField(max_length=100, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    material_party = models.ForeignKey(MaterialParty, on_delete=models.CASCADE,
                                       null=True, blank=True, related_name='materials')

    def save(self, *args, **kwargs):
        code_name_validate(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Warehouse(BaseModel):
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    can_import = models.BooleanField(default=True)
    can_export = models.BooleanField(default=True)
    use_negative = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        code_name_validate(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Device(BaseModel):
    agent = models.ForeignKey('hr.Employee', on_delete=models.CASCADE)
    imei = models.CharField(max_length=16, unique=True, validators=[
        validators.RegexValidator(
            regex=r'^\d{16}$',
            message='IMEI должен состоять из 16 цифр.',
            code='invalid_imei'
        )
    ])
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.agent


class Currency(BaseModel):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        code_name_validate(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Dealer(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
