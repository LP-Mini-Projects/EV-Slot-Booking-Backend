from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    # extra fields
    email = models.EmailField(primary_key=True, )
    phone = models.IntegerField(default=0)
    pincode = models.IntegerField(default=000000)

    def __str__(self):
        return self.email