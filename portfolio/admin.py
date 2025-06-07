from django.contrib import admin

# Register your models here.
admin.site.site_header = "Yémalin Morel KPAVODE's Portfolio"
admin.site.site_title = "Yémalin Morel KPAVODE's Portfolio"
admin.site.index_title = "Welcome to Yémalin Morel KPAVODE's Portfolio"

from .models import Tag, SkillCategory, Skill, LanguageProficiency, Project, Experience, Certification, ContactInfo, Education, Transcript

admin.site.register(Tag)
admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(LanguageProficiency)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Certification)
admin.site.register(ContactInfo)
admin.site.register(Education)
admin.site.register(Transcript)