from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='rota/login.html'), name='login'),
    path('dashboard/', views.index, name='dashboard'),  # User dashboard
    path('manage_rota/', views.manage_rota, name='manage_rota'),
    path('request_day/', views.request_day, name='request_day'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
