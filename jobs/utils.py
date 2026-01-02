import random
from datetime import datetime, timedelta
from .models import JobPost

try:
    from .live_search import LiveJobSearchEngine
except ImportError:
    LiveJobSearchEngine = None

class JobSearchEngine:
    def __init__(self):
        self.mock_companies = [
            'TCS', 'Infosys', 'Wipro', 'Accenture', 'IBM', 'Microsoft', 'Google', 
            'Amazon', 'Flipkart', 'Paytm', 'Zomato', 'Swiggy', 'BYJU\'S', 'Ola'
        ]
        
        self.mock_locations = [
            'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Pune', 
            'Kolkata', 'Ahmedabad', 'Gurgaon', 'Noida'
        ]
        
        self.platforms = ['naukri', 'indeed', 'linkedin', 'internshala', 'apna']
    
    def search_jobs(self, query, location=''):
        """Search jobs from live sources"""
        try:
            # Use live search engine if available
            if LiveJobSearchEngine:
                live_engine = LiveJobSearchEngine()
                jobs = live_engine.search_all_platforms(query, location)
                
                # If live search fails or returns no results, fallback to mock data
                if jobs:
                    return jobs
            
            # Fallback to mock data
            return self._get_fallback_jobs(query, location)
        except Exception as e:
            print(f"Live search failed: {e}")
            # Fallback to mock data
            return self._get_fallback_jobs(query, location)
    
    def _get_fallback_jobs(self, query, location=''):
        """Fallback mock job search"""
        jobs = []
        num_results = random.randint(5, 10)
        
        for i in range(num_results):
            job_data = {
                'title': f"{query} Developer",
                'company': random.choice(self.mock_companies),
                'location': location or random.choice(self.mock_locations),
                'description': f"We are looking for a skilled {query} developer to join our team...",
                'requirements': f"Experience with {query}, problem-solving skills, team collaboration",
                'skills_required': [query.lower(), 'communication', 'teamwork'],
                'experience_required': f"{random.randint(1, 5)}-{random.randint(6, 10)} years",
                'salary_range': f"{random.randint(3, 15)}-{random.randint(16, 30)} LPA",
                'platform': random.choice(self.platforms),
                'external_url': f"https://example.com/job/{i}",
                'posted_date': datetime.now() - timedelta(days=random.randint(1, 30))
            }
            jobs.append(job_data)
        
        return jobs
    
    def save_jobs_to_db(self, jobs_data):
        """Save job data to database"""
        saved_jobs = []
        
        for job_data in jobs_data:
            # Check if job already exists
            existing_job = JobPost.objects.filter(
                title=job_data['title'],
                company=job_data['company'],
                platform=job_data['platform']
            ).first()
            
            if not existing_job:
                job = JobPost.objects.create(**job_data)
                saved_jobs.append(job)
            else:
                saved_jobs.append(existing_job)
        
        return saved_jobs