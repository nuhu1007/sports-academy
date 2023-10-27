from django.db import models

from altar.models.players import Player

# Create here
class Game(models.Model):
    opponent = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100, null=True, blank=True)
    result = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField()
    scorers = models.ManyToManyField(Player, related_name='scorers')
    highlights = models.FileField(upload_to='media/game_highlights/', blank=True)

    def __str__(self):
        return f"Game vs {self.opponent}, on {self.date} at {self.time}"