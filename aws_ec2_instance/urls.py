from django.urls import path
from . import views

urlpatterns = [
    path('<str:instance_id>/', views.check_instance_creation_date, name='check_instance_creation_date')
]
