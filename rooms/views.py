from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,HttpResponse
import pytz
from .models import RoomTypes,Rooms,MaintenanceRooms,countMaintenanceRoomsInPeriod
from django.db.models import F
from reservation.models import Perma_Reservation, countPermaResInPeriod,countTempResInPeriod
from django.contrib import messages

from datetime import date, datetime

# Create your views here.

def check_type_variables(price ,beds ,max_guests ,desc):
    result = {}

    print(int(price))

    if not (price and beds and max_guests and desc):
        result['bool'] = False
        print(price)
        print(max_guests)
        print(beds)
        print(desc)
        result['massege'] = 'There Are Missing Fields'
        return result

    if int(price) <= 0 or int(beds) <= 0 or int(max_guests) <= 0:
        result['bool'] = False
        result['massege'] = 'All Numeric Values Must Be A Non Zero Positive'
        return result

    else:
        result['bool'] = True
        return result

def check_room_varible(type,floor):
    result = {}
    if type and floor:
        result['bool'] = True
        return result


    elif not (type or floor):
        result['bool'] = False
        result['massege'] = 'There Are Missing Fields'
        return result

    elif floor <= 0 :
        result['bool'] = False
        result['massege'] = 'Floor Sould Be A Non Zero Positive'


def check_maintenance_variables(start,end):
    start_date = date(int(start[0:4]),int(start[5:7]),int(start[8:]))
    end_date = date(int(end[0:4]),int(end[5:7]),int(end[8:]))
    print(start_date)
    print(end_date)
    result = {}
    if start and end:
        result['bool'] = True
        

    elif (not start) or (not end):
        result['bool'] = False
        result['massege'] = 'There Are Missing Fields'
        

    if end_date < start_date:
        result['bool'] = False
        result['massege'] = 'End Date Cannot Be Less Than Start Date'

    print(datetime.now(pytz.timezone('UTC')).date())
    if start_date < datetime.now(pytz.timezone('UTC')).date():
        result['bool'] = False
        result['massege'] = 'Start Date Cannot Be Less Than Today'

    if end_date < datetime.now(pytz.timezone('UTC')).date():
        result['bool'] = False
        result['massege'] = 'End Date Cannot Be Less Than Today'

    return result
        

    

def check_room_before_operation(id,temp_start_date,temp_end_date):
    start_date = date(int(temp_start_date[0:4]),int(temp_start_date[5:7]),int(temp_start_date[8:]))
    end_date = date(int(temp_end_date[0:4]),int(temp_end_date[5:7]),int(temp_end_date[8:]))
    room = Rooms.objects.get(id = id)
    room_type = room.type
    in_maintenance = MaintenanceRooms.objects.filter(
        room = room,
        start_date__lte = end_date,
        end_date__gte = start_date
    ).exists()
    print(in_maintenance)

    in_reservation = Perma_Reservation.objects.filter(
        active = True,
        room = room,
        start_date__lte = end_date,
        end_date__gte = start_date
    ).exists()
    print(in_reservation)

    current_maintenance = countMaintenanceRoomsInPeriod(start_date,end_date,room_type.name)
    print(current_maintenance)
    temp_res = countTempResInPeriod(start_date,end_date,room_type.name)
    print(temp_res)
    perm_res = countPermaResInPeriod(start_date,end_date,room_type.name)
    print(perm_res)

    check_count = (current_maintenance + temp_res + perm_res) < room_type.count

    return (not in_maintenance) and check_count and (not in_reservation)

#Views Start Here
@login_required()
def home(request):
    context = {}
    context['rooms'] = Rooms.objects.all()
    context['total'] = Rooms.objects.all().count()
    context['available'] = Rooms.objects.filter(state = Rooms.EMPTY).count()
    context['maintenance'] = Rooms.objects.filter(state = Rooms.UNDER_MAINTENANCE).count()
    context['reserved'] = Rooms.objects.filter(state = Rooms.INHABITED).count()
    return render(request,'rooms home.html',context)

def room_types(request):
    context = {}
    context['roomtypes'] = RoomTypes.objects.all()
    context['total'] = Rooms.objects.all().count()
    context['available'] = Rooms.objects.filter(state = Rooms.EMPTY).count()
    context['maintenance'] = Rooms.objects.filter(state = Rooms.UNDER_MAINTENANCE).count()
    context['reserved'] = Rooms.objects.filter(state = Rooms.INHABITED).count()
    return render(request,'room types.html',context)

@login_required()
def add_room_type(request):
    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')

    if request.method=='GET':
        return render(request,'add room type.html')

    elif request.method=='POST':
        #check = check_type_variables(request.POST.get('name'),request.FILES.get('image'),request.POST.get('price'),request.POST.get('size'),request.POST.get('beds'),request.POST.get('max guests'),request.POST.get('desc'),False)
        #if not check['bool']:
         #   return render(request,'add room type.html',check)

        new_type=RoomTypes()
        new_type.name = request.POST['name']
        new_type.image = request.FILES['image']
        new_type.price = int(request.POST['price'])
        new_type.size = int(request.POST['size'])
        new_type.beds = int(request.POST['beds'])
        new_type.count = 0
        new_type.max_guests = int(request.POST['max guests'])
        new_type.desc = request.POST['desc']
        new_type.save()
        return redirect('add type')


@login_required()
def add_room(request):
    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
        
    context = {}
    context['types'] = RoomTypes.objects.all()
    if request.method=='GET':
        return render(request,'add room.html',context)
    else:
        check = check_room_varible(request.POST.get('type'),request.POST.get('floor'))
        if not check['bool']:
            context['massege'] = check['massege']
            return render(request,'add room.html',context)

        new_room=Rooms()
        new_room.type = RoomTypes.objects.get(name = request.POST['type'])
        RoomTypes.objects.filter(name = request.POST['type']).update(count = F('count') +1)
        new_room.floor = int(request.POST['floor'])
        new_room.save()
        return render(request,'add room.html',context)

@login_required()
def maintenance(request,id):
    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
        

    if request.method == 'POST':
        check = check_maintenance_variables(request.POST.get('firstdate'),request.POST.get('lastdate'))
        if not check['bool']:
            messages.error(request,check['massege'])
            return redirect('rooms home')

        if check_room_before_operation(id , request.POST['firstdate'] , request.POST['lastdate']):
            temp = request.POST['firstdate']
            start_date = date(int(temp[0:4]),int(temp[5:7]),int(temp[8:]))
            new_maintenance = MaintenanceRooms()
            new_maintenance.room = Rooms.objects.get(id = id)
            new_maintenance.start_date = request.POST['firstdate']
            new_maintenance.end_date = request.POST['lastdate']
            new_maintenance.save()
            if start_date == date.today():
                Rooms.objects.filter(id = id).update(state = Rooms.UNDER_MAINTENANCE)

            massege = 'Room Added To Maintenance'
            messages.success(request,massege)
            return redirect('rooms home')

        else:
            print("maintenance")
            messages.error(request,'this room is either already in maintenance or reserved in the given date period')
            return redirect('rooms home')

        
@login_required()
def delete_type(request, name):
    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
        
    context = {}
    if request.method=='GET':
        type = RoomTypes.objects.get(name = name)
        context['type'] = type
        return render(request,'delete room type.html',context)
    
@login_required()
def commit_type_delete(request,name):
    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
        
    context = {}
    type_del = RoomTypes.objects.get(name = name)
    type_del.delete()
    massege = 'Room Type Deleted Successfully'
    context['RoomTypes'] = RoomTypes.objects.all()
    context['massege'] = massege
    return render(request,'rooms home.html',context)


@login_required()
def update_type(request, name):
    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
        
    if request.method=='POST':
        check = check_type_variables(request.POST.get('price'),request.POST.get('bed'),request.POST.get('people'),request.POST.get('description'))
        type =RoomTypes.objects.get(name = name)
        if not check['bool']:
            messages.error(request,check['massege'])
            return redirect('room types')

        if 'photo' in request.FILES:
            type.image = request.FILES['photo']

        type.price = request.POST['price']
        type.beds = request.POST['bed']
        type.max_guests = request.POST['people']
        type.desc = request.POST['description']
        type.save()

        messages.success(request,'Type Updated Successfully')
        return redirect('room types')


    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
        
    context = {}

    check = check_type_variables(request.POST.get('price'),request.POST.get('size'),request.POST.get('beds'),request.POST.get('max guests'),request.POST.get('desc'),True)
    type =RoomTypes.objects.get(name = name)
    if not check['bool']:
        check['type'] = type
        return render(request,'update room type.html',check)

    if 'image' in request.FILES:
        type.image = request.FILES['image']
        
    type.price = request.POST['price']
    type.beds = request.POST['beds']
    type.max_guests = request.POST['max guest']
    type.desc = request.POST['desc']
    type.save()

    massege = 'Room Type Updated Successfully'

    context['RoomTypes'] = RoomTypes.objects.all()
    context['massege'] = massege

    return render(request,'rooms home.html',context)