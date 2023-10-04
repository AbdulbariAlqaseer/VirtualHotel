from time import timezone
from .models import Offer
from rooms.models import RoomTypes
from datetime import datetime
import pytz


def deactivate_offer():
    offers = Offer.objects.filter(end_date__lt= datetime.now(pytz.timezone('UTC')).date())
    for offer in offers:
        RoomTypes.objects.filter(offer = offer).update(offer = None)

    Offer.objects.filter(end_date__lt= datetime.now(pytz.timezone('UTC')).date()).delete()
    print("Task 'deactivate_offer' Successfull")
    