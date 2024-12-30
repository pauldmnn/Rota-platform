from django.contrib import admin
from .models import StaffProfile


class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone_number', 'address')
    search_fields = ('user__username', 'email')


admin.site.register(StaffProfile, StaffProfileAdmin)
