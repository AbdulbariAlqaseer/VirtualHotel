from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='rooms home'),
    path('roomtypes/',views.room_types,name='room types'),
    path('addtype/',views.add_room_type,name='add type'),
    path('addroom/',views.add_room,name='add room'),
    path('maintenance/<int:id>',views.maintenance,name='maintenance'),

    #API Paths
    path('deletetype/<str:name>',views.delete_type,name='delete room type'),
    path('updatetype/<str:name>',views.update_type,name='update room type'),
    path('committypedelete/<str:name>',views.commit_type_delete,name='commit type delete'),

]