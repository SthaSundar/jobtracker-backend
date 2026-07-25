from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'status', 'date_applied', 'user', 'created_at')
    list_filter = ('status', 'date_applied')
    search_fields = ('company', 'role')
