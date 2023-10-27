from django.db import models

from altar.models.players import Player
from altar.models.branch import Branches

# Create here
class TrainingSession(models.Model):
    training_branch = models.ForeignKey(Branches, on_delete=models.CASCADE, related_name='training_branch', null=True)
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    players = models.ManyToManyField(Player, through='Attendance')
    notes = models.TextField()
    highlights = models.FileField(upload_to='media/training_highlights/', blank=True)

    def __str__(self):
        return f"Training Session for {self.training_branch.branch} branch, on {self.date}"
    

class Attendance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_attendance')
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE, related_name='session_attendance')
    attended = models.BooleanField(default=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attendance for {self.player} for {self.training_session}"