from django.urls import path
from rota import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create_staff_profile/', views.create_staff_profile, name='create_staff_profile'),
    path('view_profile/', views.view_staff_profile, name='view_staff_profile'),
    path('', views.staff_dashboard, name='staff_dashboard'),
    path('completed_shifts/', views.completed_shifts, name='completed_shifts'),
    path('request_day_off/', views.request_day_off, name='request_day_off'),
    path('admin/manage_requests/', views.admin_manage_requests, name='admin_manage_requests'),  # Manage requests
    path('login/', views.user_login, name='login'),  # Login page
    path('logout/', views.custom_logout, name='logout'),
    path('admin/create_rota/', views.admin_create_rota, name='admin_create_rota'),  # Admin rota creation
    path('admin/update_rota/<int:rota_id>/', views.update_rota, name='update_rota'),  # Update rota
    path('admin/weekly_rotas/', views.weekly_rotas, name='weekly_rotas'),
    path('admin/list_profiles/', views.list_user_profiles, name='list_user_profiles'),
    path('admin/edit_profile/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),
    path('admin/delete_profile/<int:user_id>/', views.delete_user_profile, name='delete_user_profile'),
    path('profile/', views.staff_profile, name='staff_profile'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='rota/change_password.html',
        success_url='/dashboard/'  # Redirect after successful password change
    ), name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='rota/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='rota/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='rota/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='rota/password_reset_complete.html'), name='password_reset_complete'),
]




