from django.http.response import Http404
from django.core.exceptions import ObjectDoesNotExist
from rooms.models import MaintenanceRooms, countMaintenanceRoomsInPeriod
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
from .generateCode import Code
from datetime import datetime,date,time,timedelta
from pytz import timezone
from roomservices.models import Service
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# exception for no entires, REMEBER***************************************
def check_data(date1 , date2 , typeRoom , guests):
    ''' return tuple contain boolean value and message'''

    # 1) if any data is None Which is not entered
    if not (date1 and date2 and typeRoom and guests):
        return False,"Not entered some values"
    
    # 2) discussing the two dates
    utcNow = datetime.now(timezone("UTC"))

    utcDateNow = utcNow.date()
    utcTimeNow = utcNow.time()
    nineOclock = time(21,0,0,0)

    d1 = date(int(date1[0:4]),int(date1[5:7]),int(date1[8::]))
    d2 = date(int(date2[0:4]),int(date2[5:7]),int(date2[8::]))
    
    # *** 2-1) if start date befor date of today
    if d1 < utcDateNow:
        return False,"start date is befor today"
    # *** 2-2) if the start date is the same as today's date after nine o'clock
    if d1 == utcDateNow and utcTimeNow >= nineOclock :
        return False,"It is not allowed to book a room online after nine in the evening on the same day"

    # *** 2-3) if end date befor start date
    if d1 >= d2 :
        return False,"wrong end date"

    if (d2 - d1).days > 15:
        return False,"Reservations are not allowed for more than 15 days."

    # 3) exception for type rooms if is existing or not
    try:
        objType = RoomTypes.objects.get(name = typeRoom)
    except ObjectDoesNotExist:
        return False,"type of room is not exite"
    
    # 4) discuss possibilities guests
    if int(guests) <= 0 :
        return False,"invalid value for resident"
    if int(guests) > objType.max_guests :
        return False,"The number of residents is higher than the maximum number allowed in the room"
    
    # return true and "objType" So that we do not recalculate
    return True,objType,utcNow

def check_register_age(birth_date):
    bdate =date(int(birth_date[0:4]),int(birth_date[5:7]),int(birth_date[8::]))
    today = datetime.now(timezone("UTC")).date()
    if bdate.year > (today.year - 18):
        return False
    if bdate.year == (today.year - 18):
        if bdate.month > today.month:
            return False
        if bdate.month == today.month:
            if bdate.day > today.day:
                return False
    return True

def check_data2(first_name , last_name , date_birth , date1 , date2 , typeRoom , guests ,numPassword):
    # 1) if any data is None Which is not entered
    if not (first_name and last_name and date_birth and date1 and date2 and typeRoom and guests and numPassword):
        return False,"Not entered some values"
    if not check_register_age(date_birth):
        return False,"Need To Be 18 or Older"
    # 2) discussing the two dates
    utcNow = datetime.now(timezone("UTC"))
    utcDateNow = utcNow.date()
    utcTimeNow = utcNow.time()
    
    d1 = date(int(date1[0:4]),int(date1[5:7]),int(date1[8::]))
    d2 = date(int(date2[0:4]),int(date2[5:7]),int(date2[8::]))

    if utcTimeNow >= time(12,0,0):
        if d1 < utcDateNow:
            return False,"start date is befor today"
    else:
        if d1 < utcDateNow - timedelta(days = 1):
            return False,"Vaild start date"
    
    if d1 >= d2 :
        return False,"wrong end date"
    if (d2 - d1).days > 15:
        return False,"Reservations are not allowed for more than 15 days."

    try:
        objType = RoomTypes.objects.get(name = typeRoom)
    except ObjectDoesNotExist:
        return False,"type of room is not exite"

    if int(guests) <= 0 :
        return False,"invalid value for resident"
    if int(guests) > objType.max_guests :
        return False,"The number of residents is higher than the maximum number allowed in the room"
    return True,objType,utcNow

def check_room(room , date1 , date2):
    if Perma_Reservation.objects.filter(
        active=True, room=room, start_date__lt=date2, end_date__gt=date1
        ).count() > 0 :
        return False
    if MaintenanceRooms.objects.filter(
        is_active=True, room=room, start_date__lte=date2.date(), end_date__gte=date1.date()
        ).count() > 0 :
        return False
    return True 

def add_temp_reservation(request):
    context = {}
    userFromRequest = request.user
    context['error'] = ""
    context['message'] = ""
    context['sevices'] = Service.objects.all()
    context['types'] = RoomTypes.objects.all()

    context['firstType'] = context['types'].first()
    context['types'] = context['types'][1:]
    context['lstNumType'] = [(i+1) for i in range(len(context['types']))]
    context['ziped'] = zip(context['types'],[(i+2) for i in range(len(context['types']))])

    if request.method == 'GET':
        print("get")
        return render(request,'booking.html',context)
    else:
        if not userFromRequest.is_authenticated :
            context['error']="To make a reservation, a login is required"
            print(context['error'])
            return render(request,'booking.html',context)

        #if not customer
        cus = Customers.objects.filter(Account_id = request.user)
        if cus.count()== 0:
            context['error']="Reservation for the account of the customers, not for the account of the employees"
            print(context['error'])
            return render(request,'booking.html',context)

        if Temp_Reservation.objects.filter(active = True,customer = cus[0]).__len__() >= 1 :
            context['error']="There is already a pre-booking, unfortunately the hotel policy is to have a single reservation"
            print(context['error'])
            return render(request,'booking.html',context)

        #if for vaild data
        check = check_data(
            request.POST.get("date1"),request.POST.get("date2"),
            request.POST.get("type"),request.POST.get("guests")
            )
        if not check[0] :
            context['error'] = check[1]
            print(context['error'])
            return render(request,'booking.html',context)

        objType = check[1]
        dt_now = check[2]
        d1 = request.POST['date1'].split('-')
        d2 = request.POST['date2'].split('-')
        if date(int(d1[0]),int(d1[1]),int(d1[2])) == dt_now.date() and dt_now.time().hour >= 14:
            date1 = datetime(int(d1[0]),int(d1[1]),int(d1[2]),dt_now.time().hour,dt_now.time().minute,dt_now.time().second,dt_now.time().microsecond,timezone("UTC"))
            date2 = datetime(int(d2[0]),int(d2[1]),int(d2[2]),12,0,0,0,timezone("UTC"))
        else:
            date1 = datetime(int(d1[0]),int(d1[1]),int(d1[2]),14,0,0,0,timezone("UTC"))
            date2 = datetime(int(d2[0]),int(d2[1]),int(d2[2]),12,0,0,0,timezone("UTC"))
        
        count = objType.count
        if count <= 0 :
            context['error'] = "We apologize but there are no rooms of this type available"
            print(context['error'])
            return render(request,'booking.html',context)
        
        count -= countTempResInPeriod(
            dateFirst = date1,
            dateSecond = date2,
            typeRoomName = request.POST['type']
        )
        if(count <= 0) :
            context['error'] = "We apologize but there are no rooms of this type available"
            print(context['error'])
            return render(request,'booking.html',context)
        
        count -= countPermaResInPeriod(
            dateFirst = date1,
            dateSecond = date2,
            typeRoomName = request.POST['type']
        )
        if count <= 0 :
            context['error'] = "We apologize but there are no rooms of this type available"
            print(context['error'])
            return render(request,'booking.html',context)

        count -= countMaintenanceRoomsInPeriod(
            dateFirst = date1,
            dateSecond = date2,
            typeRoomName = request.POST['type']
        )
        if count <= 0 :
            context['error'] = "We apologize but there are no rooms of this type available"
            print(context['error'])
            return render(request,'booking.html',context)
        
        #**********add*********
        t = Temp_Reservation(
            code = Code.getInstance().datetimeCode(),
            customer = cus[0],
            room_type = objType,
            start_date = date1,
            end_date = date2,
            guests = request.POST["guests"]
        )
        t.save()
        for i in context['sevices']:
            if i.name in request.POST :
                t.service.add(i)
        #send code to email
        '''mail_subject = 'Reservation Code'
        message = render_to_string('code.html', {
            'user': t.customer.Account_id,
            'code': t.code,
        })
        to_email = t.customer.Account_id.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()'''
        context['message'] = "The unique reservation code has been sent to the email to be used when confirming the reservation at the reception."
        print(context['message'])
        return render(request,'booking.html',context) 

def confirm_temp(request):
    userFromRequest = request.user
    if not userFromRequest.is_authenticated or not request.user.is_staff or request.method == 'GET':
        raise Http404("Page not found")
    if not "num_pass" in request.POST or not "code" in request.POST :
        messages.error(request,"Incomplete entry")
        return redirect('books admin')
    try:
        t = Temp_Reservation.objects.get(code = request.POST["code"])
        if t.active == False:
            messages.error(request,"Wrong : The reservation has already been cancelled.")
            return redirect('books admin')
        rooms = Rooms.objects.filter(type = t.room_type) 
        room = None
        for i in rooms:
            if check_room(i,t.start_date,t.end_date):
                room = i
                break
        if not room :
            messages.error(request,"wrong no rooms wrong in if's")
            return redirect('books admin')
        
        bill1 = t.room_type.price * (t.end_date.date() - t.start_date.date()).days
        bill2 = bill1
        if t.room_type.offer :
            bill2 = bill1 - (bill1 * t.room_type.offer.percentage/100)

        p = Perma_Reservation(
            start_date = t.start_date,
            end_date = t.end_date,
            account = t.customer.Account_id,
            visitor = None,
            bill_befor_discount = bill1,
            bill_after_discount = bill2,
            room = room,
            active = True,
            number = request.POST["num_pass"],
            guests = t.guests
        )
        p.save()
        t.active = False
        t.save()

        x = t.service.all()
        for i in x:
            p.service.add(i)
        messages.success(request," reservation confirmed\n room number :"+str(room.id)+"\nbill = "+str(bill2))
        return redirect('books admin')
    except ObjectDoesNotExist:
        messages.error(request,"There is no reservation with this code !")
        return redirect('books admin')

def add_perma_reservation(request):
    context = {}
    userFromRequest = request.user
    context['error']= ""
    context['message']= ""
    context['sevices'] = Service.objects.all()
    context['types'] = RoomTypes.objects.all()
    objAccount = None
    objVisit = None
    startDateIsToday = False
    if not userFromRequest.is_authenticated or not request.user.is_staff or request.method == 'GET':
        raise Http404("Page not found")
    elif request.method == 'POST':
        check = check_data2(
            request.POST.get('first_name'),request.POST.get('last_name'),
            request.POST.get('date_birth'),request.POST.get('date1'),request.POST.get('date2'),
            request.POST.get('type'),request.POST.get('guests'),request.POST.get("num_pass")
            )
        if not check[0]:
            messages.error(request,check[1])
            return redirect('books admin')
        objType = check[1]
        dt_now = check[2]
        d1 = request.POST['date1'].split('-')
        d2 = request.POST['date2'].split('-')
        if date(int(d1[0]),int(d1[1]),int(d1[2])) == dt_now.date() and dt_now.time().hour >= 14:
            startDateIsToday = True
            date1 = datetime(int(d1[0]),int(d1[1]),int(d1[2]),dt_now.time().hour,dt_now.time().minute,dt_now.time().second,dt_now.time().microsecond,timezone("UTC"))
            date2 = datetime(int(d2[0]),int(d2[1]),int(d2[2]),12,0,0,0,timezone("UTC"))
        else:
            date1 = datetime(int(d1[0]),int(d1[1]),int(d1[2]),14,0,0,0,timezone("UTC"))
            date2 = datetime(int(d2[0]),int(d2[1]),int(d2[2]),12,0,0,0,timezone("UTC"))

        count = objType.count
        if count <= 0 :
            messages.error(request,"We apologize but there are no rooms of this type available")
            return redirect('books admin')

        count -= countTempResInPeriod(
            dateFirst = date1,
            dateSecond = date2,
            typeRoomName = request.POST['type']
        )
        if(count <= 0) :
            messages.error(request,"We apologize but there are no rooms of this type available")
            return redirect('books admin')
        
        count -= countPermaResInPeriod(
            dateFirst = date1,
            dateSecond = date2,
            typeRoomName = request.POST['type']
        )
        if count <= 0 :
            messages.error(request,"We apologize but there are no rooms of this type available")
            return redirect('books admin')

        count -= countMaintenanceRoomsInPeriod(
            dateFirst = date1,
            dateSecond = date2,
            typeRoomName = request.POST['type']
        )
        if count <= 0 :
            messages.error(request,"We apologize but there are no rooms of this type available")
            return redirect('books admin')

        #**********add*********
        try:
            objAccount = Account.objects.get(email = request.POST['email'])
            if objAccount.first_name != request.POST['first_name'] or objAccount.last_name != request.POST['last_name']:
                raise ObjectDoesNotExist
            if Perma_Reservation.objects.filter(acoount = objAccount)[0].number != request.POST["num_pass"]:
                messages.error(request,"Passboard number not matching with previous number")
                return redirect('books admin')
        except ObjectDoesNotExist:
            d0 = request.POST['date_birth'].split('-')
            date_birth = date(int(d0[0]),int(d0[1]),int(d0[2]))
            tempObj = Perma_Reservation.objects.filter(number = request.POST["num_pass"])
            if tempObj.count() == 0 :
                objVisit = Visitors(email = request.POST.get("email"),first_name = request.POST["first_name"],last_name = request.POST["last_name"],birth_date = date_birth)
                objVisit.save()
            else:
                objVisit = tempObj[0].visitor
            objAccount = None

        #*************** specify room ******************
        rooms = Rooms.objects.filter(type = objType) 
        room = None
        for i in rooms:
            if check_room(i,date1,date2):
                room = i
                break
        if not room :
            messages.error(request,"wrong no rooms wrong in if's")
            return redirect('books admin')
        if startDateIsToday:
            room.state = Rooms.INHABITED
            room.save()
        
        bill1 = objType.price * (date2.date() - date1.date()).days
        bill2 = bill1
        if objType.offer :
            bill2 = bill1 - (bill1 * objType.offer.percentage/100)
        
        p = Perma_Reservation(
            account = objAccount,
            visitor = objVisit,
            room = room,
            start_date = date1,
            end_date = date2,
            bill_befor_discount = bill1,
            bill_after_discount = bill2,
            active = True,
            guests = request.POST["guests"],
            number = request.POST["num_pass"]
        )
        p.save()
        for i in context['sevices']:
            if i.name in request.POST :
                p.service.add(i)
        messages.success(request,"successfull \nRoom number :"+str(room.id)+"\nBill is :"+str(bill1))
        return redirect('books admin') 

def Extend_reser(request,id):
    userFromRequest = request.user
    if not userFromRequest.is_authenticated or request.method == 'GET':
        raise Http404("Page not found")
    elif request.method == 'POST':
        try:
            t = Perma_Reservation.objects.get(id = id)
            d2 = request.POST['leave'].split('-')
            date2 = datetime(int(d2[0]),int(d2[1]),int(d2[2]),12,0,0,0,timezone("UTC"))
            date1 = t.end_date.replace(hour = 14)
            objType = t.room.type
            if date2.date() <= date1.date():
                messages.error(request,"invalid end date")
                return redirect('my reservations')
            count = objType.count
            count -= countTempResInPeriod(
                dateFirst = date1,
                dateSecond = date2,
                typeRoomName = objType
            )
            if(count <= 0) :
                messages.error(request,"We apologize but there are no rooms of this type available")
                return redirect('my reservations')
            if Perma_Reservation.objects.filter(active = True,start_date__gte= date1, start_date__lt = date2,room = t.room).count() > 0 :
                messages.error(request,"We apologize but there are no rooms of this type available")
                return redirect('my reservations')
            if MaintenanceRooms.objects.filter(is_active = True,start_date__gte= date1.date(), start_date__lte = date2.date(),room = t.room).count() > 0 :
                messages.error(request,"We apologize but there are no rooms of this type available")
                return redirect('my reservations')
            bill1 = objType.price * (date2.date() - date1.date()).days
            bill2 = bill1
            if objType.offer :
                bill2 = bill1 - (bill1 * objType.offer.percentage / 100)
            t.end_date = date2
            t.bill_befor_discount = t.bill_befor_discount + bill1
            t.bill_after_discount = t.bill_after_discount + bill2
            t.save()
            messages.success(request,"It was completed")
            return redirect('my reservations')
        except ObjectDoesNotExist:
            messages.error(request,"not exists reservatin")
            return redirect('my reservations')

def delete_res(request,id):
    userFromRequest = request.user
    if not userFromRequest.is_authenticated or request.method == 'GET':
        raise Http404("Page not found")
    elif request.method == 'POST':
        try:
            t = Temp_Reservation.objects.get(id = id)
            t.active = False
            t.save()
            messages.success(request,"reservation has been canceled")
            return redirect('my reservations')
        except ObjectDoesNotExist:
            messages.error(request,"not exists reservatin")
            return redirect('my reservations')

def search(email,number):
    result = {}
    if (not email) and (not number):
        return False,None,None

    if email and (not number):
        return True,Temp_Reservation.objects.filter(customer__Account_id__email = email),None

    if (not email) and number:
        return True,None,Perma_Reservation.objects.filter(number = number)

    if email and number:
        return True,Temp_Reservation.objects.filter(account__email = email),Perma_Reservation.objects.filter(number = number)

def filter_res(month,year):
    if month and year:
        month = int(month)
        year = int(year)
        return True,Temp_Reservation.objects.filter(start_date__year = year,start_date__month = month),Perma_Reservation.objects.filter(start_date__year = year,start_date__month = month)
    return False,None,None

def show_reservations(request):
    userFromRequest = request.user
    if not userFromRequest.is_authenticated:
        raise Http404("Page not found")
    if request.method == 'GET':
        context = {}
        context['types'] = RoomTypes.objects.all()
        context['services'] = Service.objects.all()
        
        check_search = search(request.GET.get('email'),request.GET.get('number'))
        check_filter = filter_res(request.GET.get('month'),request.GET.get('year'))
        if check_search[0] and (not check_filter[0]):
            list1 = []
            if check_search[1] :
                for i in check_search[1]:
                    list1.append(i)

            list2 = []
            if check_search[2] :
                for i in check_search[2]:
                    list2.append(i)

            dif = len(list1) - len(list2)
            if dif < 0:
                for i in range(-1*dif):
                    list1.append(None)

            elif dif > 0:
                for i in range(dif):
                    list2.append(None)

            context['zip'] = zip(list1,list2)
            
        elif (not check_search[0]) and check_filter[0]:
            list1 = []
            if check_filter[1] :
                for i in check_filter[1]:
                    list1.append(i)

            list2 = []
            if check_filter[2]:
                for i in check_filter[2]:
                    list2.append(i)

            dif = len(list1) - len(list2)
            if dif < 0:
                for i in range(-1*dif):
                    list1.append(None)

            elif dif > 0:
                for i in range(dif):
                    list2.append(None)

            context['zip'] = zip(list1,list2)

        elif (not check_search[0]) and (not check_filter[0]):
            list1 = []
            for i in Temp_Reservation.objects.all():
                list1.append(i)

            list2 = []
            for i in Perma_Reservation.objects.all():
                list2.append(i)

            dif = len(list1) - len(list2)
            if dif < 0:
                for i in range(-1*dif):
                    list1.append(None)

            elif dif > 0:
                for i in range(dif):
                    list2.append(None)
            context['zip'] = zip(list1,list2)
        context['rooms'] = Rooms.objects.all()
        context['total'] = Rooms.objects.all().count()
        context['available'] = Rooms.objects.filter(state = Rooms.EMPTY).count()
        context['maintenance'] = Rooms.objects.filter(state = Rooms.UNDER_MAINTENANCE).count()
        context['reserved'] = Rooms.objects.filter(state = Rooms.INHABITED).count()
        return render(request,'books.html',context)

def update_temp_reservation(request,id):
    #raise
    userFromRequest = request.user
    if not userFromRequest.is_authenticated or (request.method=="GET"):
        raise Http404("Page not found")
    try:
        t = Temp_Reservation.objects.get(pk=id)
        check = check_data(
            request.POST.get("firstdate"),request.POST.get("lastdate"),
            request.POST.get("type"),request.POST.get("guests")
            )
        if not check[0] :
            messages.error(request,check[1])
            return redirect('my reservations')

        objType = check[1]
        dt_now = check[2]
        d1 = request.POST['firstdate'].split('-')
        d2 = request.POST['lastdate'].split('-')
        if date(int(d1[0]),int(d1[1]),int(d1[2])) == dt_now.date() and dt_now.time().hour >= 14:
            date1 = datetime(int(d1[0]),int(d1[1]),int(d1[2]),dt_now.time().hour,dt_now.time().minute,dt_now.time().second,dt_now.time().microsecond,timezone("UTC"))
            date2 = datetime(int(d2[0]),int(d2[1]),int(d2[2]),12,0,0,0,timezone("UTC"))
        else:
            date1 = datetime(int(d1[0]),int(d1[1]),int(d1[2]),14,0,0,0,timezone("UTC"))
            date2 = datetime(int(d2[0]),int(d2[1]),int(d2[2]),12,0,0,0,timezone("UTC"))
        
        count = objType.count
        if count <= 0 :
            messages.error(request,"We apologize but there are no rooms of this type available")
            return redirect('my reservations')
        x = 0
        if objType.name == t.room_type.name :
            x = 1
        count -= (countTempResInPeriod(
            dateFirst = date1,
            dateSecond = date2,
            typeRoomName = request.POST['type']
        )-x)
        if(count <= 0) :
            messages.error(request,"We apologize but there are no rooms of this type available")
            return redirect('my reservations')
        
        count -= countPermaResInPeriod(
            dateFirst = date1,
            dateSecond = date2,
            typeRoomName = request.POST['type']
        )
        if count <= 0 :
            messages.error(request,"We apologize but there are no rooms of this type available")
            return redirect('my reservations')

        count -= countMaintenanceRoomsInPeriod(
            dateFirst = date1,
            dateSecond = date2,
            typeRoomName = request.POST['type']
        )
        if count <= 0 :
            messages.error(request,"We apologize but there are no rooms of this type available")
            return redirect('my reservations')
    
        t.start_date = date1
        t.end_date = date2
        t.room_type = objType
        t.guests = request.POST["guests"]
        t.save()
        t.service.clear()
        services = Service.objects.all()
        for service in services:
            if service.name in request.POST :
                t.service.add(service)

        messages.success(request,'Reservation Updated')
        return redirect('my reservations')
    except ObjectDoesNotExist:
        messages.error(request,"the reservation not exist")
        return redirect('my reservations')
        
def check_monthly_returns(month, year):
    if (not month) or (not year):
        return False

    if month and year:
        return True

def monthly_income(request):
    context = {}
    userFromRequest = request.user
    if not userFromRequest.is_authenticated:
        raise Http404("Page not found")
    if request.method == 'GET':
        if check_monthly_returns(request.GET.get('month'),request.GET.get('year')):
            reservations = Perma_Reservation.objects.filter(start_date__year = request.GET.get('year'),start_date__month = request.GET.get('month'))
            total_sum = 0
            discount_sum = 0
            
            for reservation in reservations:
                total_sum += reservation.bill_befor_discount
                discount_sum += reservation.bill_after_discount
                
            context['month'] = request.GET['month']
            context['year'] = request.GET['year']
            context['total'] = total_sum
            context['discount'] = discount_sum
            context['winnings'] = total_sum - discount_sum
            
        context['rooms'] = Rooms.objects.all()
        context['total'] = Rooms.objects.all().count()
        context['available'] = Rooms.objects.filter(state = Rooms.EMPTY).count()
        context['maintenance'] = Rooms.objects.filter(state = Rooms.UNDER_MAINTENANCE).count()
        context['reserved'] = Rooms.objects.filter(state = Rooms.INHABITED).count()
        print( context['total'], context['available'], context['maintenance'], context['reserved'])
        return render(request,'monthly returns.html',context)

def my_reservations(request):
    context = {}
    perma = Perma_Reservation.objects.filter(account = request.user)
    temp = Temp_Reservation.objects.filter(customer__Account_id = request.user)
    types = RoomTypes.objects.all()
    services = Service.objects.all()
    context['permas'] = perma
    context['temps'] = temp
    context['types'] = types
    context['services'] = services
    return render(request,'my reservations.html',context)
