from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('<int:resume_id>/analysis/', views.get_resume_analysis, name='get_resume_analysis'),
    path('list/', views.list_resumes, name='list_resumes'),
]