from django.shortcuts import render, redirect
from django.templatetags.i18n import language
from django.http import JsonResponse, FileResponse
from django.template.loader import render_to_string
from django.utils.dateformat import DateFormat
from django.core.mail import send_mail
from django.contrib import messages
from .models import Project, Skill, Certification, Education, Experience, ContactInfo, LanguageProficiency
from collections import defaultdict
from .forms import ContactForm
import subprocess
import os
from tempfile import TemporaryDirectory

from .models import *

# Create your views here.
def home(request):
    return render(request, 'home.html')

def contact(request):
    contacts = ContactInfo.objects.all().order_by('type')
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"New message from {form.cleaned_data['name']}"
            body = (
                f"From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
                f"{form.cleaned_data['message']}"
            )
            send_mail(subject, body, form.cleaned_data['email'], ['yemalem03@gmail.com'])
            messages.success(request, "Message sent successfully. Thank you!")
            return redirect('contact')
        else:
            messages.error(request, "There was an error sending your message. Please try again.")
    else:
        form = ContactForm()
        
    return render(request, 'contact.html', {'contacts': contacts, 'form': form})

def project_list(request):
    projects = Project.objects.all().order_by('-start_date')
    for project in projects:
        if project.media and project.media.url.lower().endswith('.mp4'):
            project.is_video = True
        else:
            project.is_video = False
    return render(request, 'projects.html', {'projects': projects})

def project_json(request, pk):
    project = Project.objects.prefetch_related('tags', 'technologies').get(pk=pk)
    media_html = ""
    if project.media:
        if project.media.url.lower().endswith('.mp4'):
            media_html = f'<video src="{project.media.url}" controls width="100%"></video>'
        else:
            media_html = f'<img src="{project.media.url}" alt="{project.title}" style="max-width:100%;">'
    
    return JsonResponse({
        "title": project.title,
        "context": project.context,
        "location": project.location,
        "start_date": project.start_date.strftime("%Y-%m-%d"),
        "end_date": project.end_date.strftime("%Y-%m-%d") if project.end_date else None,
        "description": project.description,
        "technologies": [skill.name for skill in project.technologies.all()],
        "tags": [tag.name for tag in project.tags.all()],
        "github_link": project.github_link,
        "media_url": project.media.url if project.media else None,
        "media_html": media_html
    })

def skill_list(request):
    skills = Skill.objects.all()
    categorized = defaultdict(list)
    for skill in skills:
        categorized[skill.category].append(skill)

    categorized = dict(categorized)
    
    return render(request, "skills.html", {"skills_by_category": categorized})


def certification_list(request):
    
    def serialize_cert(cert):
        return {
            "id": cert.id,
            "name": cert.name,
            "provider": cert.provider,
            "date_issued": DateFormat(cert.date_issued).format("F Y"),
            "description": cert.description,
            "link": cert.link,
            "pdf": cert.pdf.url if cert.pdf else None,
            "image": cert.image.url if cert.image else None,
        }
    
    primary = Certification.objects.filter(is_primary=True).order_by('-date_issued')
    secondary = Certification.objects.filter(is_primary=False).order_by('-date_issued')
    
    all_certs = [serialize_cert(c) for c in list(primary) + list(secondary)]

    return render(request, "certifications.html", {
        "primary": primary,
        "secondary": secondary,
        "all_certs": all_certs,
    })
    
def education(request):
    education = Education.objects.all().order_by('-end_date')
    return render(request, 'education.html', {'education': education})

def experience_list(request):
    experiences = Experience.objects.all().order_by('-start_date')
    return render(request, 'experiences.html', {'experiences': experiences})

def skill_view(request):
    skills = Skill.objects.all()
    return render(request, 'portfolio/skill_view.html', {'skills': skills})

def generate_cv_pdf(request):
    educations = Education.objects.all()
    exp_pro = Experience.objects.filter(role_type__in=["Professional", "Freelance"]).order_by("-start_date")
    exp_acad = Experience.objects.filter(role_type__in=["Academic", "Internship"]).order_by("-start_date")
    projects = Project.objects.all()
    certifications = Certification.objects.all()

    # Regrouper les compétences par catégorie
    skill_map = defaultdict(list)
    for s in Skill.objects.all():
        skill_map[s.category].append(s.name)

    context = {
        "educations": educations,
        "exp_pro": exp_pro,
        "exp_acad": exp_acad,
        "projects": projects,
        "certifications": certifications,
        "skills_by_category": dict(skill_map),
    }

    with TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "cv.tex")
        pdf_path = os.path.join(tmpdir, "cv.pdf")

        # Générer le fichier LaTeX à partir du template
        with open(tex_path, "w") as f:
            f.write(render_to_string("latex/resume.tex", context))

        # Compiler avec pdflatex
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_path],
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return FileResponse(open(pdf_path, "rb"), content_type='application/pdf')