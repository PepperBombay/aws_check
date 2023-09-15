from django.urls import path
from . import views

urlpatterns = [
    path('security/<str:security_group_id>/', views.get_security_group_info, name='get_security_group_info'),
]
