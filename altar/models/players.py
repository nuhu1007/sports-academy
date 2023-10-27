from django.db import models

from altar.models.branch import Branches
from altar.models.category import Categories

# Create here
class Player(models.Model):
    full_name = models.CharField(max_length=150, blank=False, null=False)
    date_of_birth = models.CharField(max_length=100, blank=False, null=False)
    home_address = models.CharField(max_length=200, blank=False, null=False)
    school_attended = models.CharField(max_length=200, blank=False, null=False)
    player_position = models.CharField(max_length=100, null=True, blank=True)
    player_image = models.ImageField(upload_to='media/player_images/', blank=True)
    birth_certificate = models.FileField(upload_to='media/birth_certificates/', blank=True)
    player_category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name='player_category')
    player_branch = models.ForeignKey(Branches, on_delete=models.CASCADE, blank=True, null=True, related_name='players')
    medical_condition = models.BooleanField(default=False, blank=True)
    medical_condition_details = models.CharField(max_length=500, blank=True, null=True)
    parent_full_name = models.CharField(max_length=150, blank=False, null=False)
    parent_phone_number = models.CharField(max_length=20, blank=False, null=False)
    emergency_contact = models.CharField(max_length=20, blank=False, null=False)
    email_address = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_separation = models.DateTimeField(null=True, blank=True)
    date_of_reactivation = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return str(self.full_name)