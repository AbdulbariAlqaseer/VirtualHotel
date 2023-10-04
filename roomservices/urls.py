from django.urls import path
from . import views

urlpatterns = [
    path('',views.service_home,name='service home'),
    path('deleteservice/<int:id>',views.delete_service,name='delete service')
]