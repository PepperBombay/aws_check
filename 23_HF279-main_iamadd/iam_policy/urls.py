# iam_policy/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('Root_MFA_Check/', views.Root_MFA_Check, name='Root_MFA_Check'),
]