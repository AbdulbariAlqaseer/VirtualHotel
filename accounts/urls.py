from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('misc/',views.misc,name='misc'),
    path('about/',views.about,name = 'about'),
    path('register/',views.registration_view,name='register'),
    path('logout/',views.logout_view,name = 'logout'),
    path('login/',views.login_view, name='login'),
    path('activate/<str:uidb64>/<str:token>',views.activate, name='activate'),
    path('addstaff/',views.register_staff,name='add staff'),
    path('showstaff/',views.show_staff,name='show staff'),

    #test URL
    path('verificate/',views.verificate,name='verificate'),

    # API URLS
    path('updatestaff/',views.update_staff,name='update staff'),
    path('deletestaff/',views.show_delete,name='show delete'),
    path('deletestaff/<int:id>',views.delete_staff,name='delete staff'),
    path('updatespecific/<int:id>',views.update_specific_staff,name='update specific'),
]