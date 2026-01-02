from django.db import models

class JobPost(models.Model):
    PLATFORM_CHOICES = [
        ('naukri', 'Naukri'),
        ('internshala', 'Internshala'),
        ('indeed', 'Indeed'),
        ('linkedin', 'LinkedIn'),
        ('apna', 'Apna'),
    ]
    
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    skills_required = models.JSONField(default=list)
    experience_required = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100, blank=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    external_url = models.URLField()
    posted_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.company} ({self.platform})"

class JobSearch(models.Model):
    query = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    results_count = models.IntegerField(default=0)
    searched_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Search: {self.query} - {self.results_count} results"