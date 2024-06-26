from django.db import models
from django.contrib.auth.models import User

# example locations used in order to test out different temperatures and weather conditions
class LocationChoices(models.TextChoices):
    LONDON = 'london', 'London'
    BERLIN = 'berlin', 'Berlin'
    PARIS = 'paris', 'Paris',
    DUBAI = 'dubai', 'Dubai',
    STOCKHOLM = 'stockholm', 'Stockholm'

class Task(models.Model):
    # delete all tasks once user deleted, blank=True - should be changed in production system
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True) 
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=20, choices = LocationChoices.choices, null=True)

    def __str__(self):
        return self.title

    class Meta:
        # order data by completed
        ordering = ['completed'] 
