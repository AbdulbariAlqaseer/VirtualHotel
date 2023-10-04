from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.offer_home,name='offer home'),
    path('addoffer/',views.add_offer,name='add offer'),
]