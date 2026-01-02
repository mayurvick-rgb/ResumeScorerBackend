from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import JobPost, JobSearch
from .serializers import JobPostSerializer, JobSearchSerializer
from .utils import JobSearchEngine

@api_view(['GET'])
def search_jobs(request):
    query = request.GET.get('query', '')
    location = request.GET.get('location', '')
    
    if not query:
        return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search for jobs
    search_engine = JobSearchEngine()
    jobs_data = search_engine.search_jobs(query, location)
    
    # Save jobs to database
    saved_jobs = search_engine.save_jobs_to_db(jobs_data)
    
    # Record search
    JobSearch.objects.create(
        query=query,
        location=location,
        results_count=len(saved_jobs)
    )
    
    # Serialize and return results
    serializer = JobPostSerializer(saved_jobs, many=True)
    return Response({
        'query': query,
        'location': location,
        'results_count': len(saved_jobs),
        'results': serializer.data
    })

@api_view(['GET'])
def get_job_details(request, job_id):
    try:
        job = JobPost.objects.get(id=job_id)
        serializer = JobPostSerializer(job)
        return Response(serializer.data)
    except JobPost.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_recent_searches(request):
    searches = JobSearch.objects.order_by('-searched_at')[:10]
    serializer = JobSearchSerializer(searches, many=True)
    return Response(serializer.data)