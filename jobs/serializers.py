from rest_framework import serializers
from .models import JobPost, JobSearch

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = [
            'id', 'title', 'company', 'location', 'description', 'requirements',
            'skills_required', 'experience_required', 'salary_range', 'platform',
            'external_url', 'posted_date', 'created_at'
        ]

class JobSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSearch
        fields = ['id', 'query', 'location', 'results_count', 'searched_at']