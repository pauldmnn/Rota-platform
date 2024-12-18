from django.urls import path
from rota import views

urlpatterns = [
    # Staff dashboard (default view for logged-in staff users)
    path('', views.staff_dashboard, name='staff_dashboard'),

    # View completed shifts
    path('completed_shifts/', views.completed_shifts, name='completed_shifts'),

    # Request a day off
    path('request_day_off/', views.request_day_off, name='request_day_off'),

    # Admin functionalities
    path('admin/manage_requests/', views.admin_manage_requests, name='admin_manage_requests'),  # Manage requests
    path('admin/weekly_rota/', views.admin_weekly_rota, name='admin_weekly_rota'),  # View weekly rota
    path('admin/update_rota/<int:rota_id>/', views.update_rota, name='update_rota'),  # Update rota

    # Other functionality can be added here as needed
]
