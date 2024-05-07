from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import Customers

class CustomerAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            customer = Customers.objects.get(username=username, password=password)
            return customer
        except Customers.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Customers.objects.get(pk=user_id)
        except Customers.DoesNotExist:
            return None