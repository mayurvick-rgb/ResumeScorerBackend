from django.contrib import admin
from .models import JobPost, JobSearch

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'platform', 'location', 'posted_date']
    list_filter = ['platform', 'posted_date', 'created_at']
    search_fields = ['title', 'company', 'location']
    readonly_fields = ['created_at']

@admin.register(JobSearch)
class JobSearchAdmin(admin.ModelAdmin):
    list_display = ['query', 'location', 'results_count', 'searched_at']
    list_filter = ['searched_at']
    search_fields = ['query', 'location']