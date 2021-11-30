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
    station_name = models.CharField(max_length=20,default = 'EV Station')
    phone_no = models.IntegerField(default=0)
    location = models.TextField(max_length = 100,default = None)
    working_hours = models.CharField(max_length=20,default = '9:00 am to 11:00 pm')
    star_rating = models.CharField(null=True ,max_length = 2)  #To be calculated as average of all ratings
    active_status = models.BooleanField(default = True)
    photos = models.ImageField(upload_to = 'stations/',blank = True)

class Review(models.Model):
    STARS = (('1',1),('2',2),('3',3),('4',4),('5',5))
    written_by = models.ForeignKey(User,null = True, on_delete=models.CASCADE)
    about = models.ForeignKey(Station,null = True, on_delete=models.CASCADE)
    rating = models.CharField(max_length = 10,default = '3', choices=STARS)
    feedback = models.TextField(max_length=100, blank = True)

class Plug(models.Model):
    PLUGS = (('IEC-60309','IEC-60309'),
    ('IEC-62196(AC type 2)','IEC-62196(AC type 2)'),
    ('3 Pin Connector(15 Amp)','3 Pin Connector(15 Amp)'),
    ('CSS connector','CSS connector'),
    ('GBT connector','GBT connector'),
    ('CHAdeMO connector','CHAdeMO connector'))

    station_name = models.ForeignKey(Station,null = True,on_delete=models.CASCADE)
    charger_type = models.CharField(default = 'IEC-62196(AC type 2)',max_length = 25,choices = PLUGS)
    charging_speed = models.FloatField(default = 0) #kW
    charging_rate = models.FloatField(default = 0) #Rupees per 15 min
    booking_status = models.BooleanField(default = False)

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

