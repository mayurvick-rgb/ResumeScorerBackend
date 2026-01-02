from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user_email = models.EmailField()
    file = models.FileField(upload_to='resumes/')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Resume - {self.user_email} - {self.original_filename}"

class ResumeAnalysis(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    extracted_text = models.TextField()
    skills = models.JSONField(default=list)
    experience_years = models.FloatField(default=0)
    education = models.JSONField(default=list)
    contact_info = models.JSONField(default=dict)
    
    def __str__(self):
        return f"Analysis - {self.resume.original_filename}"