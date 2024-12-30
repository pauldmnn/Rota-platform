from django.urls import path
from rota import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create_staff_profile/', views.create_staff_profile, name='create_staff_profile'),
    path('admin/allocated_shifts/', views.admin_allocated_shifts, name='admin_allocated_shifts'),
    path('view_profile/', views.view_staff_profile, name='view_staff_profile'),
    path('home/', views.home, name='home'),
    path('completed_shifts/', views.completed_shifts, name='completed_shifts'),
    path('request_day_off/', views.request_day_off, name='request_day_off'),
    path('admin/manage_requests/', views.admin_manage_requests, name='admin_manage_requests'),
    path('login/', views.user_login, name='login'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('admin/create_rota/', views.admin_create_rota, name='admin_create_rota'),  
    path('admin/update_rota/<int:rota_id>/', views.update_rota, name='update_rota'), 
    path('admin/weekly_rotas/', views.weekly_rotas, name='weekly_rotas'),
    path('admin/update_rota_inline/', views.update_rota_inline, name='update_rota_inline'),
    path('admin/list_profiles/', views.list_user_profiles, name='list_user_profiles'),
    path('admin/edit_profile/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),
    path('admin/delete_profile/<int:user_id>/', views.delete_user_profile, name='delete_user_profile'),
    path('view_staff_profile/', views.view_staff_profile, name='view_staff_profile'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path("password-reset/", views.password_reset_request, name="password_reset_request"),
    path('lockout/', TemplateView.as_view(template_name='rota/lockout.html'), name='lockout'),
    path('admin/update_rota/<int:rota_id>/', views.update_rota, name='update_rota'),
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='rota/change_password.html',
        success_url='/view_staff_profile/'  # Redirect to the user's profile after password change
    ), name='change_password'),

]




