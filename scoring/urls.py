from django.urls import path
from . import views

urlpatterns = [
    path('calculate/', views.calculate_score, name='calculate_score'),
    path('resume/<int:resume_id>/', views.get_resume_scores, name='get_resume_scores'),
    path('analytics/<int:resume_id>/', views.get_analytics, name='get_analytics'),
    path('comparison/<int:resume_id>/', views.get_score_comparison, name='get_score_comparison'),
]