from django.contrib import admin
from .models import Rota, Request

@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'shift_type', 'start_time', 'end_time')
    list_filter = ('shift_type', 'date')
    search_fields = ('user__username',)

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




