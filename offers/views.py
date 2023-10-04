from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import request
from django.shortcuts import render,redirect,HttpResponse
from .models import Offer
from datetime import date
from rooms.models import RoomTypes,Rooms
from django.contrib import messages
    

def check_offer_variables(name ,percentage ,end_date):
    result = {}
    if not (name and percentage and end_date):
        result['bool'] = False
        result['massege'] = 'There Are Missing Fields'
        return result

    elif int(percentage) <=0 or int(percentage) >=100:
        result['bool'] = False
        result['massege'] = 'The Percentage Needs To Be Between But Not Equal To 0 And 100'
        return result

    else:
        result['bool'] = True
        return result

# Create your views here.

@login_required()
def offer_home(request):
    user = request.user
    context = {}
    if not user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
    
    if user.is_superuser and user.is_authenticated and request.method=='GET':
        context['offers'] = Offer.objects.all()
        context['types'] = RoomTypes.objects.filter(offer = None)
        context['all_types'] = RoomTypes.objects.all()
        context['total'] = Rooms.objects.all().count()
        context['available'] = Rooms.objects.filter(state = Rooms.EMPTY).count()
        context['maintenance'] = Rooms.objects.filter(state = Rooms.UNDER_MAINTENANCE).count()
        context['reserved'] = Rooms.objects.filter(state = Rooms.INHABITED).count()
        return render(request,'offers.html',context)

@login_required()
def add_offer(request):
    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')

    
    if request.method=='POST':
        check = check_offer_variables(request.POST.get('name'),request.POST.get('percentage'),request.POST.get('lastdate'))
        if not check['bool']:
            messages.error(request,check['massege'])
            return redirect('offer home')

        new_offer = Offer()
        new_offer.name = request.POST['name']
        new_offer.percentage = request.POST['percentage']
        new_offer.end_date = request.POST['lastdate']
        types = RoomTypes.objects.all()
        test = False
        for type in types:
            if type.name in request.POST:
                if test == False:
                    test = True
                    new_offer.save()

                type.offer = new_offer
                type.save()

        if not test:
            messages.error(request,'You Must Enter At Least One Room Type For The Offer')
            return redirect('offer home')

        messages.success(request,'Offer Added Successfully')
        return redirect('offer home')



    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
        
    context = {}
    deleted = Offer.objects.get(id = id)
    deleted.delete()
    massege = 'Offer Deleted Successfully'
    offers = Offer.objects.all()
    context['offers'] = offers
    context['massege'] = massege
    return render(request,'offer Home.html',context)