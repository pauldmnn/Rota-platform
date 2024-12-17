from django.urls import path
from . import views 


urlpatterns = [
    path('', views.staff_dashboard, name='staff_dashboard'),
    path('completed_shifts/', views.completed_shifts, name='completed_shifts'),
    path('admin/staff_requests/', views.admin_staff_requests, name='admin_staff_requests'),
    path('admin/weekly_rota/', views.admin_weekly_rota, name='admin_weekly_rota'),
]


