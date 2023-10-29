from django.urls import path
from . import views

urlpatterns = [
    path('<str:instance_id>/', views.check_ami_public, name='check_ami_public'),
]
