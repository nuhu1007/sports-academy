from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(_('First Name'), max_length=100, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=100, blank=True, null=True)
    email = models.EmailField(_('Email Address'), unique=True, null=False, db_index=True)
    phone_number = models.CharField(_('Phone Number'), max_length=100, blank=False, null=False)
    national_id = models.IntegerField(_('National Identification Number'), blank=True, null=True)
    image = models.ImageField(upload_to='media/profile_pics/', blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)