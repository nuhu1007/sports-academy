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
    medical_condition = models.BooleanField(default=False, blank=True)
    medical_condition_details = models.CharField(max_length=500, blank=True, null=True)
    parent_full_name = models.CharField(max_length=150, blank=False, null=False)
    parent_phone_number = models.CharField(max_length=20, blank=False, null=False)
    emergency_contact = models.CharField(max_length=20, blank=False, null=False)
    email_address = models.EmailField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return str(self.full_name)
    

class Game(models.Model):
    opponent = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100, null=True, blank=True)
    result = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField()
    highlights = models.FileField(upload_to='media/game_highlights/', blank=True)

    def __str__(self):
        return f"Game vs {self.opponent} on {self.date} at {self.time}"
    

class TrainingSession(models.Model):
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    players = models.ManyToManyField(Player, through='Attendance')
    notes = models.TextField()
    highlights = models.FileField(upload_to='media/training_highlights/', blank=True)

    def __str__(self):
        return f"Training Session on {self.date} at {self.location}"
    

class Attendance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_attendance')
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE, related_name='session_attendance')
    attended = models.BooleanField(default=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attendance for {self.player} for {self.training_session}"