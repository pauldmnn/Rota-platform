from django.contrib import admin
from .models import Rota, Request

@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'shift_type', 'is_updated')
    list_filter = ('is_updated', 'shift_type', 'date')
    search_fields = ('user__username',)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_day', 'status')
    list_filter = ('status',)
    search_fields = ('user__username',)
