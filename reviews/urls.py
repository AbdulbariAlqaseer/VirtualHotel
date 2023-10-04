from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.reviews_home,name='reviews home'),
    path('addreview/',views.add_review,name='add review'),
    path('viewreviews/',views.my_reviews,name='view my reviews'),
    path('updatereview/<int:id>',views.update_review,name='update review'),
]