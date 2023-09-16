from django.urls import path
from . import views

urlpatterns = [
    path('<str:security_group_id>/', views.get_security_group_info, name='get_security_group_info'),
]
