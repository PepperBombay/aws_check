# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('check_vpc_subnets/', views.check_vpc_subnets, name='check_vpc_subnets'),
]
