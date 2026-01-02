from django.db import models
from resumes.models import Resume
from jobs.models import JobPost

class ResumeScore(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    ats_score = models.FloatField()
    skill_match_score = models.FloatField()
    experience_score = models.FloatField()
    overall_score = models.FloatField()
    recommendations = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['resume', 'job_post']
    
    def __str__(self):
        return f"Score: {self.overall_score} - {self.resume.original_filename} vs {self.job_post.title}"

class ScoreAnalytics(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    total_applications = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    top_matching_roles = models.JSONField(default=list)
    skill_gaps = models.JSONField(default=list)
    improvement_suggestions = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics - {self.resume.original_filename}"