
from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

def is_pos(value):
    if value < 0:
        raise ValidationError("value is negative")
    return value

class RoomTypes(models.Model):
    name = models.CharField(verbose_name='name',max_length=50,primary_key=True)
    image = models.ImageField(upload_to = 'room pics')
    price = models.IntegerField(verbose_name='price',validators=[is_pos])
    size = models.IntegerField(verbose_name='Size',validators=[is_pos])
    beds = models.SmallIntegerField(verbose_name='beds',validators=[is_pos])
    count = models.IntegerField(verbose_name='count',validators=[is_pos])
    max_guests = models.IntegerField(verbose_name='max guests',validators=[is_pos])
    desc = models.TextField(verbose_name='Description')
    offer = models.ForeignKey("offers.Offer",on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def offer_price(self):
        if self.offer:
            discount = self.price * (self.offer.percentage/100)
            return self.price - discount

        else:
            return self.price

class Rooms(models.Model):
    type = models.ForeignKey("RoomTypes",on_delete=models.SET_NULL,null=True)
    floor = models.SmallIntegerField(validators=[is_pos])
    UNDER_MAINTENANCE = "1"
    INHABITED = "2"
    EMPTY = "3"
    CHOICES_STATE = [
        (UNDER_MAINTENANCE,"Under maintenance"),
        (INHABITED,"Inhabited"),
        (EMPTY,"Empty")
    ]
    state = models.CharField(max_length=1,choices=CHOICES_STATE,default="3")
    def stateName(self):
        choice = self.state
        length = len(self.CHOICES_STATE)
        for i in range(length):
            if choice == self.CHOICES_STATE[i][0] :
                return self.CHOICES_STATE[i][1]
    def stateChoice(name):
        length = len(Rooms.CHOICES_STATE)
        for i in range(length):
            if name == Rooms.CHOICES_STATE[i][1] :
                return Rooms.CHOICES_STATE[i][0]
    def __str__(self):
        return "floor:{},state:{}".format(self.floor,self.stateName())

class MaintenanceRooms(models.Model):
    room = models.ForeignKey('Rooms',on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

def countMaintenanceRoomsInPeriod(dateFirst,dateSecond,typeRoomName):
    '''return count of maintenance rooms in specifc period'''
    return MaintenanceRooms.objects.filter(
        room__type = typeRoomName,
        start_date__lte = dateSecond,
        end_date__gte = dateFirst
    ).__len__()