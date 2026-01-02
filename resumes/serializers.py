from rest_framework import serializers
from .models import Resume, ResumeAnalysis

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'user_email', 'file', 'original_filename', 'uploaded_at', 'processed']
        read_only_fields = ['id', 'uploaded_at', 'processed']

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = ['id', 'resume', 'extracted_text', 'skills', 'experience_years', 'education', 'contact_info']