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
        return obj.date.strftime("%A") 
    day.short_description = "Day of Week"


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Request model.
    """
    list_display = ('user', 'requested_day', 'status', 'comment')  
    list_filter = ('status', 'requested_day')  
    search_fields = ('user__username',)  
    ordering = ('requested_day', 'user') 




