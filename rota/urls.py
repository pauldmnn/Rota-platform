from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('completed_shifts/', views.completed_shifts, name='completed_shifts'),
    path('login/', views.custom_login, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('manage_requests/', views.manage_requests, name='manage_requests'),  # Admin request management
]
