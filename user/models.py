from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True,blank=True)
    phone=models.CharField(max_length=20,unique=False,null=False,blank=False)
    name=models.CharField(max_length=15,unique=False,null=False,blank=False)
    profile_pic = models.ImageField(
    upload_to='profile_pics/',
    default='profile_pics/cat.png',
    null=True,
    blank=True
)
    def __str__(self):
        return self.username
