from django.apps import apps
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Login(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=15)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    objects = BaseUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class User(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='user')
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='users/')
    phone = models.CharField(max_length=200)
    cart = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Location(models.Model):
    location = models.CharField(max_length=100)

class Theater(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='theater')
    theater_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='theater/')
    contact = models.CharField(max_length=20)
    # location = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='theaters')
    about = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.theater_name
