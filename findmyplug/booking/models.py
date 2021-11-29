from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):

    # extra fields
    email = models.EmailField(primary_key=True, )
    phone = models.IntegerField(default=0)
    pincode = models.IntegerField(default=000000)

    def __str__(self):
        return self.email

class Vehicle(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='Vehicle', on_delete=models.CASCADE)
    registration_no = models.CharField(primary_key = True, max_length=11, unique=True)
    vehicle_identification_no = models.CharField(max_length=17, unique=True)
    vehicle_model = models.CharField(max_length = 30)
    plug_type = models.CharField(max_length=20)

class Station(models.Model):
    pass

class Review(models.Model):
    pass

class Plug(models.Model):
    pass

class Booking(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    station = models.OneToOneField(Station, related_name='Station', on_delete=models.CASCADE)
    plug = models.OneToOneField(Plug,related_name='Plug', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    units = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits = 6, decimal_places = 2)

class Payment(models.Model):
    payment_of = models.OneToOneField(Booking, on_delete=models.CASCADE)
    total_amt = models.DecimalField(max_digits = 6, decimal_places = 2)
    payment_status = models.BooleanField()

