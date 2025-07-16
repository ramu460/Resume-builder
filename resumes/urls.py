
from .views import download_resume_pdf
from django.urls import path
from .import views

urlpatterns = [
    path('', views.resume_list, name='resume_list'),
    path('new/', views.create_resume, name='create_resume'),
    path('<int:pk>/', views.resume_detail, name='resume_detail'),
    path('<int:pk>/edit/', views.edit_resume, name='edit_resume'),
    path('<int:pk>/delete/', views.delete_resume, name='delete_resume'),
    path('<int:pk>/preview/', views.preview_resume, name='preview_resume'),
    path('<int:pk>/download/', views.download_resume_pdf, name='download_resume'),
    path('<int:pk>/templates/', views.choose_template, name='choose_template'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),

    path('api/get-states/<str:country_code>/', views.get_states, name='get_states'),
    path('api/get-countries/', views.get_countries, name='get_countries'),
]
