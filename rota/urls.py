from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"), 
    path("manage_tota/", views.manage_rota, name="manage_rota"),
    path("request_day/", views.request_day, name="request_day"),
]