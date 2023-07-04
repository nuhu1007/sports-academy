from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    username = models.CharField(_('Username'), max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(_('First Name'), max_length=100, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=100, blank=True, null=True)
    email = models.EmailField(_('Email Address'), unique=True, null=False, db_index=True)
    phone_number = models.CharField(_('Phone Number'), max_length=100, blank=False, null=False)
    national_id = models.IntegerField(_('National Identification Number'), blank=True, null=True)
    image = models.ImageField(upload_to='media/profile_pics/', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)
    

class Categories(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.category)
    

class Player(models.Model):
    full_name = models.CharField(max_length=150, blank=False, null=False)
    date_of_birth = models.CharField(max_length=100, blank=False, null=False)
    home_address = models.CharField(max_length=200, blank=False, null=False)
    school_attended = models.CharField(max_length=200, blank=False, null=False)
    player_position = models.CharField(max_length=100, null=True, blank=True)
    player_category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name='player_category')
    medical_condition = models.BooleanField(default=False)
    parent_full_name = models.CharField(max_length=150, blank=False, null=False)
    parent_phone_number = models.CharField(max_length=20, blank=False, null=False)
    emergency_contact = models.CharField(max_length=20, blank=False, null=False)
    email_address = models.EmailField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return str(self.full_name)
    