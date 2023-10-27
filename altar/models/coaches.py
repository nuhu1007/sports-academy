from django.db import models

from altar.models.branch import Branches
from altar.models.category import Categories

# Create here
class Coach(models.Model):
    full_name = models.CharField(max_length=150, blank=False, null=False)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    coach_image = models.ImageField(upload_to='media/coach_images/', blank=True, null=True)
    coaching_category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name='coaching_category')
    coaching_branch = models.ForeignKey(Branches, on_delete=models.CASCADE, blank=True, null=True, related_name='coaches')
    cv = models.FileField(upload_to='media/coach_cv/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_separation = models.DateTimeField(null=True, blank=True)
    date_of_reactivation = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return str(self.full_name)