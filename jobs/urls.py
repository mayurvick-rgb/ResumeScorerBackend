from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_jobs, name='search_jobs'),
    path('<int:job_id>/', views.get_job_details, name='get_job_details'),
    path('recent-searches/', views.get_recent_searches, name='get_recent_searches'),
]