from django.urls import path
from resumes.api.views import (
    ResumeListCreateView, ResumeDetailView,
    EducationListCreateView, EducationDetailView,
    ExperienceListCreateView, ExperienceDetailView,
    SkillListCreateView, SkillDetailView,
    ProjectListCreateView, ProjectDetailView,
    CertificationListCreateView, CertificationDetailView, TestThrottleView,
    get_countries, get_states
)

urlpatterns = [

    path('api/resumes/', ResumeListCreateView.as_view(), name='api-resume-list'),
    path('api/resumes/<int:pk>/', ResumeDetailView.as_view(), name='api-resume-detail'),

    path('api/resumes/<int:resume_id>/education/', EducationListCreateView.as_view(), name='api-education-list'),
    path('api/education/<int:pk>/', EducationDetailView.as_view(), name='api-education-detail'),

    path('api/resumes/<int:resume_id>/experience/', ExperienceListCreateView.as_view(), name='api-experience-list'),
    path('api/experience/<int:pk>/', ExperienceDetailView.as_view(), name='api-experience-detail'),

    path('api/resumes/<int:resume_id>/skill/', SkillListCreateView.as_view(), name='api-skill-list'),
    path('api/skill/<int:pk>/', SkillDetailView.as_view(), name='api-skill-detail'),

    path('api/resumes/<int:resume_id>/project/', ProjectListCreateView.as_view(), name='api-project-list'),
    path('api/project/<int:pk>/', ProjectDetailView.as_view(), name='api-project-detail'),

    path('api/resumes/<int:resume_id>/certification/', CertificationListCreateView.as_view(), name='api-certification-list'),
    path('api/certification/<int:pk>/', CertificationDetailView.as_view(), name='api-certification-detail'),

    path('api/countries/', get_countries, name='api-countries'),

    path('api/test-throttle/', TestThrottleView.as_view(), name='test-throttle'),
    
]