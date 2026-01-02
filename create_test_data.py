import os
import django
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_scorer.settings')
django.setup()

from jobs.models import JobPost
from datetime import datetime

def create_test_jobs():
    """Create some test job posts for demonstration"""
    
    test_jobs = [
        {
            'title': 'Python Developer',
            'company': 'TechCorp',
            'location': 'Bangalore',
            'description': 'We are looking for a skilled Python developer with experience in Django, Flask, and REST APIs.',
            'requirements': 'Python, Django, Flask, REST API, PostgreSQL, Git',
            'skills_required': ['python', 'django', 'flask', 'rest api', 'postgresql', 'git'],
            'experience_required': '2-4 years',
            'salary_range': '8-15 LPA',
            'platform': 'naukri',
            'external_url': 'https://example.com/job/1',
            'posted_date': datetime.now()
        },
        {
            'title': 'React Developer',
            'company': 'StartupXYZ',
            'location': 'Mumbai',
            'description': 'Frontend developer needed with React, JavaScript, and modern web technologies.',
            'requirements': 'React, JavaScript, HTML, CSS, Node.js, Redux',
            'skills_required': ['react', 'javascript', 'html', 'css', 'nodejs', 'redux'],
            'experience_required': '1-3 years',
            'salary_range': '6-12 LPA',
            'platform': 'linkedin',
            'external_url': 'https://example.com/job/2',
            'posted_date': datetime.now()
        },
        {
            'title': 'Full Stack Developer',
            'company': 'InnovateTech',
            'location': 'Delhi',
            'description': 'Full stack developer with experience in both frontend and backend technologies.',
            'requirements': 'Python, React, Django, JavaScript, PostgreSQL, AWS',
            'skills_required': ['python', 'react', 'django', 'javascript', 'postgresql', 'aws'],
            'experience_required': '3-5 years',
            'salary_range': '12-20 LPA',
            'platform': 'indeed',
            'external_url': 'https://example.com/job/3',
            'posted_date': datetime.now()
        }
    ]
    
    created_jobs = []
    for job_data in test_jobs:
        job, created = JobPost.objects.get_or_create(
            title=job_data['title'],
            company=job_data['company'],
            defaults=job_data
        )
        if created:
            created_jobs.append(job)
            print(f"Created job: {job.title} at {job.company}")
        else:
            print(f"Job already exists: {job.title} at {job.company}")
    
    return created_jobs

if __name__ == '__main__':
    print("Creating test job data...")
    jobs = create_test_jobs()
    print(f"Created {len(jobs)} new jobs")
    print("Test data creation complete!")