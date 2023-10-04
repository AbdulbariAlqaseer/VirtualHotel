from django.urls import path
from . import views

urlpatterns = [
    path('add_reservation/', views.add_temp_reservation, name = 'add temp reservation'),
    path('add_perma/',views.add_perma_reservation,name = 'add perma reservation'),
    path('admin_booking/',views.show_reservations,name = 'books admin'),
    path('deletetemp/<int:id>',views.delete_res,name = 'delete reservation'),
    path('extendres/<int:id>',views.Extend_reser,name='extend reservation'),
    path('updateres/<int:id>',views.update_temp_reservation,name='update reservation'),
    path('monthlyreturns/',views.monthly_income,name='monthly returns'),
    path('confirm_reservation/',views.confirm_temp,name = "confirm res"),
    path('myreservations/',views.my_reservations,name='my reservations'),
]