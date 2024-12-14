from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_login, name='login'),  # Root login page
    path('dashboard/', views.index, name='dashboard'),  # User dashboard
    path('manage_rota/', views.manage_rota, name='manage_rota'),  # Admin rota management
    path('request_day/', views.request_day, name='request_day'),  # Staff request days
    path('logout/', views.logout_view, name='logout'),  # Logout view
]
