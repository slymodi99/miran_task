from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers.user import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=250, blank=True)
    user_phone = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=255, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'user_phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_phone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address_title = models.CharField(max_length=255)
    address_details = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.user_phone
