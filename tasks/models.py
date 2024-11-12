from django.db import models

# Create your models here.
class Task(models.Model):
    STATUS_CHOICE = [
        ('P', 'Pending'),
        ('C', 'Completed')
    ]
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICE)