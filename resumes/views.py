import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import Resume, ResumeAnalysis
from .serializers import ResumeSerializer, ResumeAnalysisSerializer
from .utils import ResumeProcessor

@api_view(['POST'])
def upload_resume(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    user_email = request.data.get('user_email', 'anonymous@example.com')
    
    # Validate file type
    allowed_extensions = ['.pdf', '.doc', '.docx']
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in allowed_extensions:
        return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create resume record
    resume = Resume.objects.create(
        user_email=user_email,
        file=file,
        original_filename=file.name
    )
    
    # Process resume
    try:
        processor = ResumeProcessor()
        file_path = resume.file.path
        analysis_data = processor.process_resume(file_path, file_extension)
        
        # Create analysis record
        ResumeAnalysis.objects.create(
            resume=resume,
            **analysis_data
        )
        
        resume.processed = True
        resume.save()
        
        serializer = ResumeSerializer(resume)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_resume_analysis(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        analysis = ResumeAnalysis.objects.get(resume=resume)
        
        resume_serializer = ResumeSerializer(resume)
        analysis_serializer = ResumeAnalysisSerializer(analysis)
        
        return Response({
            'resume': resume_serializer.data,
            'analysis': analysis_serializer.data
        })
    
    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)
    except ResumeAnalysis.DoesNotExist:
        return Response({'error': 'Analysis not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_resumes(request):
    resumes = Resume.objects.filter(processed=True).order_by('-uploaded_at')
    serializer = ResumeSerializer(resumes, many=True)
    return Response(serializer.data)