from django.db import models
from django.core.validators import RegexValidator, URLValidator, validate_email, FileExtensionValidator
from django.core.exceptions import ValidationError
from cloudinary_storage.storage import MediaCloudinaryStorage

"""
Django Models for Yémalin Morel KPAVODE's Portfolio Website
------------------------------------------------------------

This module defines the data schema used to manage and display content on Yémalin Morel KPAVODE's personal portfolio website.
The portfolio highlights his academic background, technical skills, professional experience, research projects, certifications,
and contact information.

Models
------

1. Tag:
    - A reusable label or keyword to categorize skills, projects, and experiences.
    - Examples: 'Computer Vision', 'NLP', 'AI', 'Africa', 'Open Source'.

2. Skill:
    - Represents a technical or methodological competency.
    - Categorized as: 'AI', 'Data Science', 'Web/DevOps', or 'Tools'.
    - Examples: 'PyTorch', 'Docker', 'FastAPI', 'TensorFlow'.

3. LanguageProficiency:
    - Stores language skills and the level of fluency.
    - Example: 'Français (Natif)', 'Anglais (B1)'.

4. Education:
    - Academic background with details about degrees, institutions, and study periods.
    - Example: 'Licence en Mathématiques Fondamentales, FAST (2020–2023)'.

5. Experience:
    - Professional or academic experience entries, including freelance work and internships.
    - Examples include backend development for the Pehu platform or statistical analysis for LESCAL.

6. Project:
    - Research or personal projects, particularly those in AI, image captioning, and African culture valorization.
    - Includes technologies used and GitHub links.
    - Example: 'Isheero – Système d’annotation automatique d’images africaines'.

7. Certification:
    - External certifications related to Data Science, AI, or other fields.
    - Example: 'IBM Data Science Certificate (2025)'.

8. ContactInfo:
    - Stores personal contact details such as email, phone number, LinkedIn, and GitHub.
    - Meant for display on the website and potentially in the footer or contact section.

Usage
-----
These models serve to dynamically populate the portfolio website and allow for future extensions, such as blog posts, articles, or
API endpoints for public project access.

Author: Yémalin Morel KPAVODE
Email: yemalem03@gmail.com
GitHub: https://github.com/yemal22
LinkedIn: https://www.linkedin.com/in/morel-kpavode
Date: May 2025
"""

def validate_contact_value(contact_type, value):
    if contact_type == "email":
        validate_email(value)
    elif contact_type == "phone" or contact_type == "whatsapp":
        phone_regex = RegexValidator(
            regex=r"^\+?\d{7,15}$",
            message="Le numéro doit être valide, ex: +22995754157."
        )
        phone_regex(value)
    elif contact_type in {"linkedin", "github", "facebook", "instagram", "twitter"}:
        url_validator = URLValidator()
        url_validator(value)
    else:
        raise ValidationError("Type de contact non supporté.")

class Tag(models.Model):
    """
    A reusable label or keyword to categorize skills, projects, and experiences.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class SkillCategory(models.Model):
    """
    Categorized as: 'AI', 'Data Science', 'Web/DevOps', or 'Tools'.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"

class Skill(models.Model):
    """
    Represents a technical or methodological competency.
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Class Font Awesome (ex: 'fab fa-python', 'fas fa-database')"
    )


    def __str__(self):
        return self.name

class LanguageProficiency(models.Model):
    """
    Stores language skills and the level of fluency.
    """
    language = models.CharField(max_length=50)
    proficiency = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.language} ({self.proficiency})'

    class Meta:
        verbose_name = "Language Proficiency"
        verbose_name_plural = "Language Proficiencies"
        
class Transcript(models.Model):
    """
    Academic transcript PDF files optionally linked to an education institution or diploma.
    """
    label = models.CharField(max_length=255, help_text="e.g. 'Semestre 1', 'Final transcript'")
    file = models.FileField(
        upload_to='transcripts/',
        validators=[FileExtensionValidator(['pdf'])],
        storage=MediaCloudinaryStorage(),
        help_text="Transcript file in PDF"
    )
    education = models.ForeignKey(
        'Education',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transcripts'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

class Education(models.Model):
    """
    Academic background with details about degrees, institutions, and study periods.
    """
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    
    logo = models.ImageField(
        upload_to='logos/',
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
        help_text="Logo of the institution"
    )
    
    diploma = models.FileField(
        upload_to='diplomas/',
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf'])],
        help_text="Diploma document (PDF)"
    )

    def __str__(self):
        return f'{self.degree} at {self.institution}'

class Experience(models.Model):
    """
    Professional or academic experience entries, including freelance work and internships.
    """
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    role_type = models.CharField(max_length=50, choices=[('Academic', 'Academic'), ('Freelance', 'Freelance'), ('Internship', 'Internship'), ('Professional', 'Professional')])
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.title} at {self.company}'

class Project(models.Model):
    """
    Research or personal projects, particularly those in AI, image captioning, and African culture valorization.
    """
    title = models.CharField(max_length=255)
    context = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    github_link = models.URLField(blank=True)
    technologies = models.ManyToManyField(Skill)
    tags = models.ManyToManyField(Tag)
    media = models.FileField(
        upload_to='projects/',
        storage=MediaCloudinaryStorage(),
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov'])]
    )

    def __str__(self):
        return self.title

class Certification(models.Model):
    """
    External certifications related to Data Science, AI, or other fields.
    """
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    date_issued = models.DateField()
    description = models.TextField()
    link = models.URLField()
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='certifications/', storage=MediaCloudinaryStorage(), null=True, blank=True)
    
    pdf = models.FileField(
        upload_to='certifications/',
        storage=MediaCloudinaryStorage(),
        null=True, blank=True,
        validators=[FileExtensionValidator(['pdf'])]
    )

    is_primary = models.BooleanField(default=False, help_text="Mark as main certification")

class ContactInfo(models.Model):
    """
    Stores personal contact details such as email, phone number, LinkedIn, and GitHub, ...
    """
    CONTACT_TYPE_CHOICES = [
        ("email", "Email"),
        ("phone", "Telephone"),
        ("linkedin", "LinkedIn"),
        ("github", "GitHub"),
        ("whatsapp", "WhatsApp"),
        ("instagram", "Instagram"),
        ("twitter", "Twitter"),
        ("facebook", "Facebook"),
    ]

    ICON_MAP = {
        "email": "fas fa-envelope",
        "phone": "fas fa-phone",
        "linkedin": "fab fa-linkedin",
        "github": "fab fa-github",
        "whatsapp": "fab fa-whatsapp",
        "instagram": "fab fa-instagram",
        "twitter": "fab fa-twitter",
        "facebook": "fab fa-facebook",
    }

    type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def clean(self):
        validate_contact_value(self.type, self.value)

    def __str__(self):
        return f'{self.type.capitalize()}: {self.value}'

    @property
    def icon(self):
        return self.ICON_MAP.get(self.type, "fas fa-address-card")


