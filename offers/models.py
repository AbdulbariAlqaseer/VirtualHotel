from django.db import models

# Create your models here.

class Offer(models.Model):
    name = models.CharField(help_text="Trade name for this offer",max_length=25)
    percentage = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)