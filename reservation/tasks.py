from accounts.models import Account
from .models import Perma_Reservation,Temp_Reservation
from rooms.models import Rooms
from datetime import date, datetime
import pytz

def resolve_perma():
    reservations = Perma_Reservation.objects.filter(end_date__lte = datetime.now(pytz.timezone('UTC')),active = True)
    for res in reservations:
        Rooms.objects.filter(id = res.room.id).update(state = Rooms.EMPTY)

    Perma_Reservation.objects.filter(end_date__lte = datetime.now(pytz.timezone('UTC')),active = True).update(active = False)

    activate = Perma_Reservation.objects.filter(start_date__lte = datetime.now(pytz.timezone('UTC')))
    for res in activate:
        Rooms.objects.filter(id = res.room.id).update(state = Rooms.INHABITED)

    print("Task 'resolve_perma' Successful")


def resolve_temp():
    Temp_Reservation.objects.filter(end_date__lte = datetime.now(pytz.timezone('UTC')),active = True).update(active = False)
    print("Task 'resolve_temp' Successfull")