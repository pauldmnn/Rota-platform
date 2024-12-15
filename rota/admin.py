from django.contrib import admin
from .models import Rota, Request

@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Rota model.
    """
    list_display = ('user', 'day', 'date', 'shift_type', 'start_time', 'end_time')  # Columns to display
    list_filter = ('date', 'shift_type')  # Filters in the admin sidebar
    search_fields = ('user__username',)  # Search bar to find rotas by username
    ordering = ('date', 'user')  # Default ordering

    def day(self, obj):
        """
        Display the day of the week for the rota date.
        """
        return obj.date.strftime("%A")  # e.g., Monday, Tuesday
    day.short_description = "Day of Week"


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Request model.
    """
    list_display = ('user', 'requested_day', 'status', 'comment')  # Columns to display
    list_filter = ('status', 'requested_day')  # Filters in the admin sidebar
    search_fields = ('user__username',)  # Search bar to find requests by username
    ordering = ('requested_day', 'user')  # Default ordering
