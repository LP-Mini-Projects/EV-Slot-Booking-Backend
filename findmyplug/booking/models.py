from datetime import datetime
from django.core.files import storage
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token

from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

# Create your models here.

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        #email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username=None

    # extra fields
    email = models.EmailField(("Email Address"),primary_key=True)
    phone = models.BigIntegerField(default=976934295)
    pincode = models.IntegerField(default=00000)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        token = Token.objects.get(user=User.objects.get(self.id))
        return token

PLUGS = (('IEC-60309','IEC-60309'),
    ('IEC-62196(AC type 2)','IEC-62196(AC type 2)'),
    ('3 Pin Connector(15 Amp)','3 Pin Connector(15 Amp)'),
    ('CSS connector','CSS connector'),
    ('GBT connector','GBT connector'),
    ('CHAdeMO connector','CHAdeMO connector'))

class Vehicle(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='User', on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=11, unique=True)
    vehicle_identification_no = models.CharField(max_length=17, unique=True)
    vehicle_model = models.CharField(max_length = 30)
    plug_type = models.CharField(default = 'IEC-62196(AC type 2)',max_length = 25,choices = PLUGS)

    def __str__(self):
        return self.vehicle_model

class Station(models.Model):
    station_name = models.CharField(max_length=100,default = 'EV Station')
    phone_no = models.IntegerField(default=0)
    location = models.TextField(max_length = 100,default = None)
    city = models.CharField(max_length=50,default='Mumbai')
    working_hours = models.CharField(max_length=20,default = '9:00 am to 11:00 pm')
    star_rating = models.CharField(null=True ,max_length = 2)  #To be calculated as average of all ratings
    active_status = models.BooleanField(default = True)
    photos = models.ImageField(upload_to = 'stations/',blank = True, storage=gd_storage)
    
    def __str__(self):
        return self.station_name

class Review(models.Model):
    STARS = (('1',1),('2',2),('3',3),('4',4),('5',5))
    written_by = models.ForeignKey(User,null = True, on_delete=models.CASCADE)
    about = models.ForeignKey(Station,null = True, on_delete=models.CASCADE)
    rating = models.CharField(max_length = 10,default = '3', choices=STARS)
    feedback = models.TextField(max_length=100, blank = True)

    def __str__(self):
        return self.written_by

class Plug(models.Model):

    station_name = models.ForeignKey(Station,null = True,on_delete=models.CASCADE)
    charger_type = models.CharField(default = 'IEC-62196(AC type 2)',max_length = 25,choices = PLUGS)
    charging_speed = models.FloatField(default = 0) #kW
    charging_rate = models.FloatField(default = 0) #Rupees per 15 min

    def __str__(self):
        return self.charger_type

class Slot(models.Model):
    plug = models.ForeignKey(Plug,related_name='Plug',on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    booking_status = models.BooleanField(default = False)

class Booking(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    station = models.ForeignKey(Station,on_delete=models.CASCADE)
    plug = models.ForeignKey(Plug,related_name='Booking_Plug',on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot,related_name='Slot',on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits = 6, decimal_places = 2)

    def __str__(self):
        return f'{self.plug} by {self.owner} '

class Payment(models.Model):
    payment_of = models.OneToOneField(Booking, on_delete=models.CASCADE)
    total_amt = models.DecimalField(max_digits = 6, decimal_places = 2)
    payment_status = models.BooleanField()

    def __str__(self):
        return f'{self.payment_of} {self.total_amt}'

