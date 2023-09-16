# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('s3-security-check/', views.s3_security_check_view, name='s3_security_check'),
]
