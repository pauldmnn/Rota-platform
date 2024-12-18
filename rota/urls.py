from django.urls import path
from rota import views


urlpatterns = [
    # Admin URLs
    path('admin/login/', views.admin_login, name='admin_login'),  # Custom admin login
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('admin/redirect/', lambda request: __import__('rota.views').views.admin_redirect_login_view(request), name='admin_redirect'),
    path('admin/weekly_rota/', views.admin_weekly_rota, name='admin_weekly_rota'),  # Weekly rota view
    path('admin/update_rota/<int:rota_id>/', views.update_rota, name='update_rota'),  # Update rota
    path('admin/logout/', views.admin_logout, name='admin_logout'),  # Admin logout
    path('admin/manage_requests/', views.admin_manage_requests, name='admin_manage_requests'),  # Manage staff requests

    # Staff URLs
    path('', views.staff_dashboard, name='staff_dashboard'),  # Staff dashboard (homepage for logged-in users)
    path('completed_shifts/', views.completed_shifts, name='completed_shifts'),  # Completed shifts
    path('request_day_off/', views.request_day_off, name='request_day_off'),  # Request day off
]
