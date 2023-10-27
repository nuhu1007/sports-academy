from django.db import models

from altar.models.branch import Branches

# Create here
class Equipments(models.Model):
    equipment_name = models.CharField(max_length=100, null=True, blank=True)
    equipment_number = models.IntegerField(default=0)
    equipment_branch = models.ForeignKey(Branches, on_delete=models.CASCADE, blank=True, null=True, related_name="equipment_branch")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.equipment_name)