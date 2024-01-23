from django.core.validators import MaxValueValidator
from django.db import models

from shared.models import BaseModel


class Division(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    amount_of_employee = models.IntegerField(validators=[MaxValueValidator(limit_value=9999)])
    divisions = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name


class Position(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(BaseModel):
    GENDER_CHOICES = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
    )

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, unique=True)
    report_card = models.IntegerField(validators=[MaxValueValidator(limit_value=999999)], unique=True)
    badge_number = models.CharField(max_length=10, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_hire = models.DateField()
    is_fired = models.BooleanField(default=False)
    date_of_fire = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    gender = models.CharField(choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    passport_number_series = models.CharField(max_length=10, unique=True)
    passport_issued_by = models.CharField(max_length=255)
    passport_when_issued = models.DateField()
    passport_pin = models.CharField(max_length=14, unique=True)
    photo = models.ImageField(upload_to='employee_photos', default='default-profile__picture.jpg')
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    warehouses = models.ManyToManyField('info.Warehouse', blank=True)

    def __str__(self):
        return self.full_name
