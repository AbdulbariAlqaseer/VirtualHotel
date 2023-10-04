from datetime import datetime
from .models import MaintenanceRooms,Rooms
import pytz

def end_maintenance():
    rooms = MaintenanceRooms.objects.filter(end_date__lt = datetime.now(pytz.timezone('UTC')).date())
    for room in rooms:
        Rooms.objects.filter(id = room.room.id).update(state = Rooms.EMPTY)

    rooms.delete()
        
    
    print("Task 'end_maintenance' Successfull")

def start_maintenance():
    rooms = MaintenanceRooms.objects.filter(start_date__lte = datetime.now(pytz.timezone('UTC')).date())
    for room in rooms:
        Rooms.objects.filter(id = room.room.id).update(state = Rooms.UNDER_MAINTENANCE)

    print("Task 'start_maintenance' Successfull")