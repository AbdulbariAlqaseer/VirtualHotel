from django.db import models
from accounts.models import Account

# Create your models here.

class Reviews(models.Model):
    Account_id = models.OneToOneField(Account,on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name='Rating')
    date = models.DateField(verbose_name='Review Date',auto_now_add=True)
    desc = models.TextField(verbose_name='Review Description')
    
