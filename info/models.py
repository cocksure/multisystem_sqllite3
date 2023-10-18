from django.db import models
from shared.models import BaseModel


class Unit(models.Model):
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# to do
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

    def __str__(self):
        return self.name


class MaterialGroup(models.Model):
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MaterialType(models.Model):
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Material(BaseModel):
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    group = models.ForeignKey(MaterialGroup, on_delete=models.CASCADE)
    type = models.ForeignKey(MaterialType, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    color = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='materials_photos', default='material_default_picture.png')

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

    def __str__(self):
        return self.name


class Device(BaseModel):
    agent = models.ForeignKey('hr.Employee', on_delete=models.CASCADE)
    imei = models.CharField(max_length=16, unique=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.agent


class Currency(BaseModel):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)

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
