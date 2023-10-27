from django.db import models

# Create here
class Categories(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.category)