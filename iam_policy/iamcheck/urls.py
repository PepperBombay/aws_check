# iamcheck/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('RootAccount_MFA_Check/', views.RootAccount_MFA_Check, name='RootAccount_MFA_Check'),
]