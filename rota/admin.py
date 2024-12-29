from django.contrib import admin
from .models import StaffProfile

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone_number', 'address')  # Fields to display
    search_fields = ('user__username', 'email')  # Allow searching by username and email

admin.site.register(StaffProfile, StaffProfileAdmin)
