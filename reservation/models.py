from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import Account,Customers
from rooms.models import RoomTypes,Rooms
from accounts.models import Visitors
from roomservices.models import Service
# Create your models here.
def is_pos(value):
    if value < 1:
        raise ValidationError("value is negative")
    return value


class Temp_Reservation(models.Model):
    code = models.CharField(max_length=13,unique=True,editable=False)
    customer = models.ForeignKey(Customers,on_delete=models.PROTECT)
    room_type = models.ForeignKey(RoomTypes,on_delete=models.SET_NULL,null=True)
    start_date = models.DateTimeField(help_text="From date")
    end_date = models.DateTimeField(help_text="To date")
    #addition = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    guests = models.SmallIntegerField(default=1,validators=[is_pos])
    service = models.ManyToManyField(Service)
    def __str__(self):
        return self.code
    class Meta:
        ordering = ["active"]


class Perma_Reservation(models.Model):
    account = models.ForeignKey(Account,on_delete=models.PROTECT,blank=True,null=True)
    visitor = models.ForeignKey(Visitors,on_delete=models.PROTECT,blank=True,null=True)
    room = models.ForeignKey(Rooms,on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    bill_befor_discount = models.IntegerField(validators=[is_pos])
    bill_after_discount = models.IntegerField(default = 0,validators=[is_pos])
    active = models.BooleanField(default=True)
    number = models.CharField(max_length=40,default="")
    service = models.ManyToManyField(Service)
    guests = models.SmallIntegerField(default=1,validators=[is_pos])
    #all_residents = models.ManyToManyField(Residents)
    def __str__(self):
        return self.id
    class Meta:
        ordering = ["active"]

def countTempResInPeriod(dateFirst,dateSecond,typeRoomName):
    '''return Count of temp reservations in specific period'''
    return Temp_Reservation.objects.filter(
        active = True ,
        start_date__lt = dateSecond ,
        end_date__gt = dateFirst ,
        room_type__name = typeRoomName
        ).__len__()

def countPermaResInPeriod(dateFirst,dateSecond,typeRoomName):
    '''return Count of perma reservations in specific period'''
    return Perma_Reservation.objects.filter(
        active = True ,
        start_date__lt = dateSecond ,
        end_date__gt = dateFirst ,
        room__type__name = typeRoomName
        ).__len__()