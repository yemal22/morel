from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project-list'),
    path('project/<int:pk>/json/', views.project_json, name='project-json'),
    path('experience/', views.experience_list, name='experience'),
    path('skills/', views.skill_list, name='skills'),
    path('education/', views.education, name='education'),
    path('certifications/', views.certification_list, name='certifications'),
    path('contact/', views.contact, name='contact'),
    path('cv/pdf/', views.generate_cv_pdf, name='resume'),
]