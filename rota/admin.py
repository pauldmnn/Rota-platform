from django.contrib import admin
from .models import Rota
# Register your models here.

@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    list_display = ('user', 'day', 'shift_type', 'start_time', 'end_time')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_day', 'status', 'comment')