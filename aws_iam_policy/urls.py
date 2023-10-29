# iam_policy/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('Root_MFA_Check/', views.Root_MFA_Check, name='Root_MFA_Check'),       #루트 MFA정책 및 사용자 루트&MFA사용 검사
    path('Password_Policy/', views.Password_Policy, name='Password_Policy'),    #패드워드 정책
]