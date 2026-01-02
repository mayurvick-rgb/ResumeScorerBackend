from rest_framework import serializers
from .models import ResumeScore, ScoreAnalytics
from jobs.serializers import JobPostSerializer

class ResumeScoreSerializer(serializers.ModelSerializer):
    job_post = JobPostSerializer(read_only=True)
    job_title = serializers.CharField(source='job_post.title', read_only=True)
    company = serializers.CharField(source='job_post.company', read_only=True)
    
    class Meta:
        model = ResumeScore
        fields = [
            'id', 'job_post', 'job_title', 'company', 'ats_score', 
            'skill_match_score', 'experience_score', 'overall_score',
            'recommendations', 'missing_skills', 'created_at'
        ]

class ScoreAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreAnalytics
        fields = [
            'id', 'total_applications', 'average_score', 'top_matching_roles',
            'skill_gaps', 'improvement_suggestions', 'updated_at'
        ]