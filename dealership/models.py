from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Department(models.Model):
    name = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('manager', 'Manager'), ('employee', 'Employee')])
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)

class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_sale = models.BooleanField(default=True)
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
