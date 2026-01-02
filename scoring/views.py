from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from resumes.models import Resume
from jobs.models import JobPost
from .models import ResumeScore, ScoreAnalytics
from .serializers import ResumeScoreSerializer, ScoreAnalyticsSerializer
from .utils import ATSScorer

@api_view(['POST'])
def calculate_score(request):
    resume_id = request.data.get('resume_id')
    job_ids = request.data.get('job_ids', [])
    
    if not resume_id or not job_ids:
        return Response({'error': 'resume_id and job_ids are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        resume = Resume.objects.get(id=resume_id)
        scorer = ATSScorer()
        scores = []
        
        for job_id in job_ids:
            try:
                job_post = JobPost.objects.get(id=job_id)
                
                # Calculate score
                score_data = scorer.calculate_overall_score(resume, job_post)
                
                if 'error' in score_data:
                    continue
                
                # Save or update score
                score, created = ResumeScore.objects.update_or_create(
                    resume=resume,
                    job_post=job_post,
                    defaults=score_data
                )
                
                scores.append(score)
            
            except JobPost.DoesNotExist:
                continue
        
        # Update analytics
        scorer.update_analytics(resume)
        
        # Serialize and return scores
        serializer = ResumeScoreSerializer(scores, many=True)
        return Response({
            'resume_id': resume_id,
            'scores': serializer.data
        })
    
    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_resume_scores(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        scores = ResumeScore.objects.filter(resume=resume).order_by('-overall_score')
        serializer = ResumeScoreSerializer(scores, many=True)
        return Response(serializer.data)
    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_analytics(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        try:
            analytics = ScoreAnalytics.objects.get(resume=resume)
            serializer = ScoreAnalyticsSerializer(analytics)
            return Response(serializer.data)
        except ScoreAnalytics.DoesNotExist:
            # Return mock analytics if none exist
            mock_analytics = {
                'total_jobs': 0,
                'average_score': 0,
                'best_score': 0,
                'improvement': 0,
                'top_skills': [],
                'missing_skills': [],
                'score_distribution': [],
                'recommendations': [
                    {
                        'title': 'Upload and analyze some jobs first',
                        'description': 'Search for jobs and calculate scores to see analytics'
                    }
                ]
            }
            return Response(mock_analytics)
    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_score_comparison(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        scores = ResumeScore.objects.filter(resume=resume)
        
        # Prepare data for charts
        chart_data = {
            'labels': [f"{score.job_post.title} - {score.job_post.company}" for score in scores],
            'ats_scores': [score.ats_score for score in scores],
            'skill_scores': [score.skill_match_score for score in scores],
            'experience_scores': [score.experience_score for score in scores],
            'overall_scores': [score.overall_score for score in scores]
        }
        
        return Response(chart_data)
    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)