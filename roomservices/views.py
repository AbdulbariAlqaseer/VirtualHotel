from django.core.checks import messages
from django.shortcuts import redirect, render,HttpResponse
from .models import Service
from django.contrib import messages
from rooms.models import Rooms

# Create your views here.
def check_service_variable(name):
    result = {}
    if not name:
        result['bool'] = False
        result['massege'] = "The Field Is Empty"
        return result

    test = Service.objects.filter(name = name).exists()

    if test:
        result['bool'] = False
        result['massege'] = 'A Service With This Name Already Exists'
        return result

    if not test:
        result['bool'] = True
        return result


def service_home(request):
    context = {}

    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')

    context['total'] = Rooms.objects.all().count()
    context['available'] = Rooms.objects.filter(state = Rooms.EMPTY).count()
    context['maintenance'] = Rooms.objects.filter(state = Rooms.UNDER_MAINTENANCE).count()
    context['reserved'] = Rooms.objects.filter(state = Rooms.INHABITED).count()
    context['services'] = Service.objects.all()
    
    if request.method == 'GET':
        return render(request,'services.html',context)
    elif request.method == 'POST':
        check = check_service_variable(request.POST.get('name'))
        if not check['bool']:
            context['error'] = check['massege']
            return render(request,'services.html',context)
        new_service = Service()
        new_service.name = request.POST['name']
        new_service.save()
        return render(request,'services.html',context)

def delete_service(request,id):
    if not request.user.is_superuser:
        return HttpResponse('You Are Not Authorized To Enter This URL')
        
    deleted = Service.objects.get(id = id)
    deleted.delete()
    messages.success(request,"Service Deleted Successfully")
    return redirect('service home')
