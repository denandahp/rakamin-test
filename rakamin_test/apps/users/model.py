
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(verbose_name='Mobile Number', max_length=20, unique=True,
                                     blank=True, null=True)
    status = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'mobile_number'


    def __str__(self) -> str:
        return self.name
