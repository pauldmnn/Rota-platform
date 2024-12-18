from django.urls import path
from rota import views

urlpatterns = [
    path('', views.staff_dashboard, name='staff_dashboard'),
    path('completed_shifts/', views.completed_shifts, name='completed_shifts'),
    path('request_day_off/', views.request_day_off, name='request_day_off'),
    path('admin/manage_requests/', views.admin_manage_requests, name='admin_manage_requests'),  # Manage requests
    path('login/', views.user_login, name='login'),  # Login page
    path('admin/create_rota/', views.admin_create_rota, name='admin_create_rota'),  # Admin rota creation
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('admin/update_rota/<int:rota_id>/', views.update_rota, name='update_rota'),  # Update rota
]
