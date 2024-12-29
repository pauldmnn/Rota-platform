"""
URL configuration for staff_rota_platform project.

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
from rota import views  # Import views from the rota app

urlpatterns = [

    # Custom admin login and dashboard
    path('admin/login/', views.admin_login, name='admin_login'),  # Custom admin login page
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('login/', views.user_login, name='login'),  # Add this line
    path('logout/', views.custom_logout, name='logout'),
    path('', views.home, name='home'),
    path('', include('rota.urls')),
]



