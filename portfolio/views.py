from django.shortcuts import render
from django.templatetags.i18n import language

from .models import *

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    languages = LanguageProficiency.objects.all()
    contacts = ContactInfo.objects.all()
    return render(request, 'portfolio/about.html', {'languages': languages, 'contacts': contacts})

def contact(request):
    contacts = ContactInfo.objects.all()
    return render(request, 'portfolio/contact.html', {'contacts': contacts})

def project_list(request):
    projects = Project.objects.all().order_by('-start_date')
    return render(request, 'portfolio/projects.html', {'projects': projects})

def skill_list(request):
    skills = Skill.objects.all()
    return render(request, 'portfolio/skills.html', {'skills': skills})

def certification_list(request):
    certifications = Certification.objects.all().order_by('-date_issued')
    return render(request, 'portfolio/certifications.html', {'certifications': certifications})

def education_list(request):
    educations = Education.objects.all().order_by('-end_date')
    return render(request, 'portfolio/educations.html', {'educations': educations})

def experience_list(request):
    experiences = Experience.objects.all()
    return render(request, 'portfolio/experiences.html', {'experiences': experiences})

def skill_view(request):
    skills = Skill.objects.all()
    return render(request, 'portfolio/skill_view.html', {'skills': skills})

def resume(request):
    return render(request, 'portfolio/resume.html')