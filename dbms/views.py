from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from .models import Customers
from django.contrib import messages
from .custom_auth import CustomerAuthenticationBackend
from .models import Tables
# Create your views here.


def dbmsreservation(request):
     return render(request,'web/reservation.html')  

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        customer = CustomerAuthenticationBackend().authenticate(request, username=username, password=password)
        if customer is not None:
            # Manually manage session
            request.session['customer_id'] = customer.customer_id
            return redirect('home')  # Redirect to a main page after login
        else:
            return render(request, 'web/index.html', {'error': 'Invalid credentials'})
    return render(request, 'web/index.html')

def home(request):
    return render(request, 'web/home.html')

def reservation(request):
    tables = Tables.objects.all()
    return render(request, 'reservation.html', {'tables': tables})

def your_reservations(request):
    return render(request,'web/your_reservation.html')