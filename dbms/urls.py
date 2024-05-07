from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservation/', views.dbmsreservation ,name = 'dbmsreservation'),
    path('home/', views.home, name='home'), 
    path('reservation/', views.reservation, name='reservation'),
    path('your-reservations/', views.your_reservations, name='your_reservations'),
    
]