from django.contrib import admin
from django.contrib.admin.sites import AdminSite
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


from django.contrib.admin import AdminSite
from django.contrib import admin

class CustomAdminSite(AdminSite):
    site_header = "Rota Management Admin"
    site_title = "Rota Platform Admin"
    index_title = "Welcome to Rota Platform Admin"

    def each_context(self, request):
        context = super().each_context(request)
        # Inject your custom CSS file
        context["css_files"] = ["/static/rota/admin.css"]  # Ensure the path matches your static setup
        return context

admin.site = CustomAdminSite(name='custom_admin')

