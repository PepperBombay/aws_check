"""
URL configuration for CloudMain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from aws_subnet_check import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aws-subnet-check/<str:vpc_id>/<str:aws_region>/', views.check_vpc_subnets, name='check_vpc_subnets'),
    path('iam_policy/', include('iam_policy.urls')),
    path('aws_s3_PublicAccess/', include('aws_s3_PublicAccess.urls')),
    path('aws_ec2_SecurityGroup/', include(aws_ec2_SecurityGroup.urls))
]
