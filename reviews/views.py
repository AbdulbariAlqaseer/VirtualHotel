from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Reviews
from rooms.models import Rooms

# Create your views here.

def check_rating(rating):
    print(rating)
    if int(rating) in (1,2,3,4,5):
        return True
    
    else:
        return False


def check_review_variables(rating ,desc ):
    result = {}
    if rating and desc:
        result['bool'] = True
        return result

    else:
        result['bool'] = False
        result['massege'] = 'There Are Missing Fields'
        return result

def check_user(user):
    exist = Reviews.objects.filter(Account_id = user).exists()
    return exist

@login_required()
def reviews_home(request):
    context = {}
    context['total'] = Rooms.objects.all().count()
    context['available'] = Rooms.objects.filter(state = Rooms.EMPTY).count()
    context['maintenance'] = Rooms.objects.filter(state = Rooms.UNDER_MAINTENANCE).count()
    context['reserved'] = Rooms.objects.filter(state = Rooms.INHABITED).count()
    reviews = Reviews.objects.all()
    context['reviews'] = reviews
    return render(request,'reviews.html',context)

@login_required()
def add_review(request):
    if request.user.is_staff:
        return HttpResponse('Staff Are Not Authorized To Enter This URL')
        
    if request.method == 'GET':
        return render(request,'user review.html')

    elif request.method == 'POST':
        if not check_rating(request.POST.get('star')):
            print(request.POST.get('star'))
            return render(request,'user review.html',{'massege':'You must enter a rating between 1 and 5'})

        check = check_review_variables(request.POST.get('star'),request.POST.get('description'))
        if not check['bool']:
            print(request.POST.get('star'))
            return render(request,'user review.html',check)
        new_review = Reviews()
        new_review.Account_id = request.user
        new_review.rating = request.POST['star']
        new_review.desc = request.POST['description']
        new_review.save()
        
        return redirect('home')


@login_required()
def my_reviews(request):
    if request.user.is_staff:
        return HttpResponse('Staff Are Not Authorized To Enter This URL')
        
    reviews = Reviews.objects.filter(Account_id = request.user)
    return render(request,'view reviews.html',{'reviews': reviews})

@login_required()
def update_review(request,id):
    if request.user.is_staff:
        return HttpResponse('Staff Are Not Authorized To Enter This URL')
        
    review = Reviews.objects.get(id = id)
    return render(request,'update review.html',{'review':review})
          