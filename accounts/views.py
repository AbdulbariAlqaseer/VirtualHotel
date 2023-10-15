from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from reviews.views import check_user
from django.contrib import messages
from datetime import date,datetime
import pytz

from accounts.forms import RegistrationForm, StaffRegistrationForm, AccountAuthenticationForm
from accounts.models import Account,Customers,Staff
from accounts.filters import filter_staff,StaffFilter
from rooms.models import RoomTypes,Rooms
from reviews.models import Reviews
from django.core.mail import EmailMessage, message
from django.http import HttpResponse

def check_register_age(temp_birth_date):
    result = {}
    birth_date = temp_birth_date
    today = datetime.now(pytz.timezone('UTC')).date()
    if birth_date.year > (today.year - 18):
        result['bool'] = False
        result['massege'] = "You Need To Be 18 or Older To Register An Account"
        return result
    
    if birth_date.year == (today.year - 18):
        if birth_date.month > today.month:
            result['bool'] = False
            result['massege'] = "You Need To Be 18 or Older To Register An Account"
            return result

        if birth_date.month == today.month:
            if birth_date.day > today.day:
                result['bool'] = False
                result['massege'] = "You Need To Be 18 or Older To Register An Account"
                return result

    result['bool'] = True
    return result

def check_staff_update(address):
    result = {}
    if not address:
        result['bool'] = False
        result['massege'] = 'You Must Input An Address'
        return result

    else:
        result['bool'] = True
        return result


# Create your views here.

def misc(request):
    if not request.user.is_staff:
        return HttpResponse('You Are Not Authorized To Enter This URL')

    context = {}
    context['total'] = Rooms.objects.all().count()
    context['available'] = Rooms.objects.filter(state = Rooms.EMPTY).count()
    context['maintenance'] = Rooms.objects.filter(state = Rooms.UNDER_MAINTENANCE).count()
    context['reserved'] = Rooms.objects.filter(state = Rooms.INHABITED).count()
    return render(request,'admin base.html',context)

def home(request):
    context = {}

    room_types = RoomTypes.objects.all()
    context['types'] = room_types
    context['reviews'] = Reviews.objects.all()
    if (request.user.id):
        context['reviewed'] = check_user(request.user)
    context['offer_types'] = RoomTypes.objects.exclude(offer = None)
    return render(request,'home.html', context)

def about(request):
    return render(request,'about.html')

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            check = check_register_age(form.cleaned_data.get('birth_date'))
            if not check['bool']:
                check['registeration_form'] = form
                return render(request,'user register.html',check)

            form.save()
            #user = form.save(commit = False)
            #user.is_active = False
            #user.save()

            cust=Customers()
            email = form.cleaned_data.get('email')
            cust.Account_id = Account.objects.get(email=email)
            cust.birth_date = form.cleaned_data.get('birth_date')
            cust.save()

            password = form.cleaned_data.get('password1')
            user = authenticate(email=email,password=password)
            login(request,user)
            return redirect('home')
            """current_site = get_current_site(request)
            mail_subject = 'Activate your Hotel account.'

            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )

            email.send()

            return HttpResponse('Please confirm your email address to complete the registration')"""

        else:
            context['registeration_form']= form
    else:
        form = RegistrationForm()
        context['registeration_form']= form
    return render(request,'user register.html',context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        print(uid)
        print(token)
        print (user)
        print('Check token:' + str(account_activation_token.check_token(user, token)))
        return HttpResponse('Activation link is invalid!')


@login_required()
def register_staff(request):

    context = {}
    user = request.user
    if user.is_authenticated and user.is_superuser:
        if request.POST:
            form = StaffRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                staff = Staff()
                staff.Account_id = Account.objects.get(email=email)
                staff.Address = form.cleaned_data.get('address')
                staff.save()
                reg = Account.objects.get(email = email)
                reg.is_admin = True
                reg.is_staff = True
                reg.save()
                return redirect('add staff')
            else:
                context['registeration_form'] = form
        else:
            form = StaffRegistrationForm()
            context['registeration_form']= form            
        return render(request,'register.html',context)
    else:
        raise UserWarning('You Are Not Authorized To Use This Functionality')


def logout_view(request):
    if request.user == AnonymousUser:
        return HttpResponse("You Are Not Logged In")
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)

            if user:
                login(request, user)
                return redirect('home')

        else:
            context['login_form'] = form
            return render(request, 'user login.html',context)

    else:
        form = AccountAuthenticationForm()

    context['login_form']= form
    return render(request, 'user login.html',context)

@login_required()
def show_staff(request):
    context = {}
    if not request.user.is_superuser :
        return HttpResponse('You Are Not Authorized To Enter This URL')

    if request.method=='GET':
        check = filter_staff(request.GET.get('address'),request.GET.get('firstname'))
        context['total'] = Rooms.objects.all().count()
        context['available'] = Rooms.objects.filter(state = Rooms.EMPTY).count()
        context['maintenance'] = Rooms.objects.filter(state = Rooms.UNDER_MAINTENANCE).count()
        context['reserved'] = Rooms.objects.filter(state = Rooms.INHABITED).count()
        if not check['bool']:
            context['staff'] = Staff.objects.all()

        else:
            context['staff'] = check['staff']
        form = StaffRegistrationForm()
        context['registeration_form']= form 
        return render(request,'staff home.html',context)

    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            staff = Staff()
            staff.Account_id = Account.objects.get(email=email)
            staff.Address = form.cleaned_data.get('address')
            staff.save()
            reg = Account.objects.get(email = email)
            reg.is_admin = True
            reg.is_staff = True
            reg.save()
            messages.success(request,'Staff Added Successfully')
            return redirect('show staff')
        else:
            context['total'] = Rooms.objects.all().count()
            context['available'] = Rooms.objects.filter(state = Rooms.EMPTY).count()
            context['maintenance'] = Rooms.objects.filter(state = Rooms.UNDER_MAINTENANCE).count()
            context['reserved'] = Rooms.objects.filter(state = Rooms.INHABITED).count()
            context['staff'] = Staff.objects.all()
            context['error_message'] = 'Account Register Failed , Check Form For Details'
            context['registeration_form'] = form

        return render(request,'staff home.html',context)

@login_required()
def update_staff(request):
    user = request.user
    if not user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')

    if user.is_authenticated and user.is_superuser and request.method=='GET':
        if 'staff email' in request.GET:
            staff = Staff.objects.get(Account_id = Account.objects.get(email=request.GET['staff email']))
            return render(request, 'update staff.html', {'staff': staff})
        else:
            return render(request,'update staff.html')

    elif user.is_authenticated and user.is_superuser and request.method=='POST':
        staff = Staff.objects.get(Account_id = Account.objects.get(email=request.POST['staff email']))
        return render(request, 'update staff.html', {'staff': staff})


@login_required()
def update_specific_staff(request,id):
    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
        
    check = check_staff_update(request.POST.get('address'))
    if not check['bool']:
        
        messages.error(request,check['massege'])
        return redirect('show staff')
        
    Staff.objects.filter(id=id).update(Address=request.POST['address'])
    messages.success(request,'Staff Updated Successfully')
    return redirect('show staff')


@login_required()
def show_delete(request):
    user = request.user
    if not user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
    
    if user.is_authenticated and user.is_superuser and request.method=='GET':
        if 'staff email' in request.GET:
            staff = Staff.objects.get(Account_id = Account.objects.get(email = request.GET['staff email']))
            return render(request, 'delete staff.html',{'staff':staff})
        
        else:
            return render(request, 'delete staff.html')

    elif user.is_authenticated and user.is_superuser and request.method=='POST':
        staff = Staff.objects.get(email = request.GET['staff email'])
        return render(request, 'delete staff.html',{'staff':staff})


@login_required()
def delete_staff(request, id):
    user = request.user
    if not user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')

    if user.is_authenticated and user.is_superuser and request.method=='POST':
        deleted = Staff.objects.get(id = id)
        account = Account.objects.get(id = deleted.Account_id.id)
        deleted.delete()
        account.delete()
        messages.success(request,'Staff Deleted Successfully') 
        return redirect('show staff')


def verificate(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        form_register = RegistrationForm()
        context['registeration_form']= form_register
        form_login = AccountAuthenticationForm()
        context['login_form'] = form_login

    elif request.method == 'POST' and 'birth_date' in request.POST:
        form = RegistrationForm(request.POST)
        print('Entered Register')

        if form.is_valid():
            check = check_register_age(form.cleaned_data.get('birth_date'))
            if not check['bool']:
                check['registeration_form'] = form
                return render(request,'register.html',check)
            user = form.save(commit = False)
            #user.is_active = False
            user.save()

            cust=Customers()
            email = form.cleaned_data.get('email')
            cust.Account_id = Account.objects.get(email=email)
            cust.birth_date = form.cleaned_data.get('birth_date')
            cust.save()

            """current_site = get_current_site(request)
            mail_subject = 'Activate your Hotel account.'

            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )

            email.send()

            return HttpResponse('Please confirm your email address to complete the registration')"""
            return redirect('home')

        else:
            context['registeration_form']= form
            context['login_form'] = AccountAuthenticationForm()

    else:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            if user:
                login(request, user)
                return redirect('home')
        
        else:
            context['login_form'] = form
            context['registeration_form'] = RegistrationForm()

    return render(request,'user login.html',context)


