from django.contrib import admin
from .models import ResumeScore, ScoreAnalytics

@admin.register(ResumeScore)
class ResumeScoreAdmin(admin.ModelAdmin):
    list_display = ['resume', 'job_post', 'overall_score', 'ats_score', 'created_at']
    list_filter = ['created_at', 'overall_score']
    search_fields = ['resume__original_filename', 'job_post__title']

@admin.register(ScoreAnalytics)
class ScoreAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['resume', 'total_applications', 'average_score', 'updated_at']
    search_fields = ['resume__original_filename']