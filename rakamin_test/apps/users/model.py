from typing import Any

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models


class CustomUserManager(UserManager):

    def create_user(self, mobile_number: str, password: str, type=None, **extra_fields: Any):
        """
        Creates and saves a User with the email and mobile_number.
        """
        user = self.model(mobile_number=mobile_number, is_superuser=False, is_active=True,
                          **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password, **extra_fields):
        user = self.create_user(mobile_number=mobile_number, password=password, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.name = user.mobile_number
        user.save(using=self._db)
        return user


class users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(verbose_name='Mobile Number', max_length=20, unique=True,
                                     blank=True, null=True)
    status = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'mobile_number'
    objects = CustomUserManager()


    def __str__(self) -> str:
        return self.name
    
    class Meta:
        app_label = 'users'