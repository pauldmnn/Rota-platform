from django.urls import path
from rota import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create_staff_profile/', views.create_staff_profile, name='create_staff_profile'),
    path('', views.staff_dashboard, name='staff_dashboard'),
    path('completed_shifts/', views.completed_shifts, name='completed_shifts'),
    path('request_day_off/', views.request_day_off, name='request_day_off'),
    path('admin/manage_requests/', views.admin_manage_requests, name='admin_manage_requests'),  # Manage requests
    path('login/', views.user_login, name='login'),  # Login page
    path('logout/', views.custom_logout, name='logout'),
    path('admin/create_rota/', views.admin_create_rota, name='admin_create_rota'),  # Admin rota creation
    path('admin/update_rota/<int:rota_id>/', views.update_rota, name='update_rota'),  # Update rota
    path('profile/', views.staff_profile, name='staff_profile'),
]



urlpatterns += [
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='rota/change_password.html',
        success_url='/dashboard/'  # Redirect after successful password change
    ), name='change_password'),
]
