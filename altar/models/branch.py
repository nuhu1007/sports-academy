from django.db import models

# Create here
class Branches(models.Model):
    branch = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.branch)