from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
from portfolio.models import *

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Python')

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Python')
        self.assertTrue(isinstance(self.tag, Tag))
        self.assertEqual(str(self.tag), 'Python')

    def test_unique_tag(self):
        with self.assertRaises(Exception):
            Tag.objects.create(name='Python')

class SkillCategoryModelTest(TestCase):
    def setUp(self):
        self.category = SkillCategory.objects.create(name='Programming Languages')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Programming Languages')
        self.assertTrue(isinstance(self.category, SkillCategory))
        self.assertEqual(str(self.category), 'Programming Languages')

    def test_verbose_names(self):
        self.assertEqual(SkillCategory._meta.verbose_name, 'Skill Category')
        self.assertEqual(SkillCategory._meta.verbose_name_plural, 'Skill Categories')

class SkillModelTest(TestCase):
    def setUp(self):
        self.category = SkillCategory.objects.create(name='Programming Languages')
        self.skill = Skill.objects.create(name='Python', category=self.category, icon='fab fa-python')

    def test_skill_creation(self):
        self.assertEqual(self.skill.name, 'Python')
        self.assertTrue(isinstance(self.skill, Skill))
        self.assertEqual(str(self.skill), 'Python')
        self.assertEqual(self.skill.category, self.category)
        self.assertEqual(self.skill.icon, 'fab fa-python')

class LanguageProficiencyModelTest(TestCase):
    def setUp(self):
        self.language = LanguageProficiency.objects.create(
            language='English',
            proficiency='B1'
        )

    def test_language_proficiency_creation(self):
        self.assertEqual(self.language.language, 'English')
        self.assertEqual(self.language.proficiency, 'B1')
        self.assertTrue(isinstance(self.language, LanguageProficiency))
        self.assertEqual(str(self.language), 'English (B1)')

    def test_verbose_names(self):
        self.assertEqual(LanguageProficiency._meta.verbose_name, 'Language Proficiency')
        self.assertEqual(LanguageProficiency._meta.verbose_name_plural, 'Language Proficiencies')

class TranscriptModelTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            institution='FAST - UAC',
            degree='Licence',
            start_date='2020-09-01',
            end_date='2023-07-01',
            location='Paris, France',
            description='desc'
        )
        self.transcript_file = SimpleUploadedFile("transcript.pdf", b"file_content", content_type="application/pdf")
        self.transcript = Transcript.objects.create(
            label='Semestre 1',
            file=self.transcript_file,
            education=self.education
        )

    def test_transcript_creation(self):
        self.assertEqual(self.transcript.label, 'Semestre 1')
        self.assertEqual(self.transcript.education, self.education)
        self.assertTrue(self.transcript.file.name.endswith('.pdf'))
        self.assertEqual(str(self.transcript), 'Semestre 1')

class EducationModelTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            institution='FAST - UAC',
            degree='Bachelier en Mathématiques Fondamentales',
            start_date='2020-09-01',
            end_date='2023-07-01',
            location='Paris, France',
            description='Description of the education'
        )

    def test_education_creation(self):
        self.assertEqual(self.education.institution, 'FAST - UAC')
        self.assertEqual(self.education.degree, 'Bachelier en Mathématiques Fondamentales')
        self.assertEqual(str(self.education), 'Bachelier en Mathématiques Fondamentales at FAST - UAC')

    def test_optional_logo_diploma(self):
        self.assertIsNone(self.education.logo)
        self.assertIsNone(self.education.diploma)

class ExperienceModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='AI')
        self.experience = Experience.objects.create(
            title='Data Scientist',
            company='Tech Company',
            role_type='Professional',
            start_date='2024-01-01',
            end_date='2024-12-31',
            location='Cotonou, Bénin',
            description='Description du poste'
        )
        self.experience.tags.add(self.tag)

    def test_experience_creation(self):
        self.assertEqual(self.experience.title, 'Data Scientist')
        self.assertEqual(self.experience.company, 'Tech Company')
        self.assertEqual(self.experience.role_type, 'Professional')
        self.assertEqual(str(self.experience), 'Data Scientist at Tech Company')
        self.assertTrue(self.experience.tags.filter(name='AI').exists())

class ProjectModelTest(TestCase):
    def setUp(self):
        self.category = SkillCategory.objects.create(name='AI')
        self.skill = Skill.objects.create(name='PyTorch', category=self.category)
        self.tag = Tag.objects.create(name='Deep Learning')
        self.project = Project.objects.create(
            title='Isheero',
            context='Research',
            start_date='2024-01-01',
            end_date='2024-12-31',
            location='Bénin',
            description='Système d\'annotation d\'images',
            github_link='https://github.com/yemal22/isheero'
        )
        self.project.technologies.add(self.skill)
        self.project.tags.add(self.tag)

    def test_project_creation(self):
        self.assertEqual(self.project.title, 'Isheero')
        self.assertEqual(str(self.project), 'Isheero')
        self.assertTrue(self.project.technologies.filter(name='PyTorch').exists())
        self.assertTrue(self.project.tags.filter(name='Deep Learning').exists())

    def test_project_optional_fields(self):
        self.assertEqual(self.project.github_link, 'https://github.com/yemal22/isheero')
        self.assertIsNone(self.project.media)

class CertificationModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Data Science')
        self.certification = Certification.objects.create(
            name='Data Science Professional Certificate',
            provider='IBM',
            date_issued='2024-01-01',
            description='Formation complète en Data Science',
            link='https://www.coursera.org/certificate/123'
        )
        self.certification.tags.add(self.tag)

    def test_certification_creation(self):
        self.assertEqual(self.certification.name, 'Data Science Professional Certificate')
        self.assertEqual(self.certification.provider, 'IBM')
        self.assertTrue(self.certification.tags.filter(name='Data Science').exists())

    def test_certification_optional_fields(self):
        self.assertIsNone(self.certification.image)
        self.assertIsNone(self.certification.pdf)
        self.assertFalse(self.certification.is_primary)

class ContactInfoModelTest(TestCase):
    def setUp(self):
        self.email_contact = ContactInfo.objects.create(
            type='email',
            value='yemalem03@gmail.com'
        )
        self.phone_contact = ContactInfo.objects.create(
            type='phone',
            value='+22995754157'
        )
        self.linkedin_contact = ContactInfo.objects.create(
            type='linkedin',
            value='https://www.linkedin.com/in/morel-kpavode'
        )

    def test_contact_info_creation(self):
        self.assertEqual(str(self.email_contact), 'Email: yemalem03@gmail.com')
        self.assertEqual(str(self.phone_contact), 'Phone: +22995754157')
        self.assertEqual(str(self.linkedin_contact), 'Linkedin: https://www.linkedin.com/in/morel-kpavode')

    def test_contact_icon_property(self):
        self.assertEqual(self.email_contact.icon, 'fas fa-envelope')
        self.assertEqual(self.phone_contact.icon, 'fas fa-phone')
        self.assertEqual(self.linkedin_contact.icon, 'fab fa-linkedin')

    def test_invalid_contact_values(self):
        with self.assertRaises(ValidationError):
            contact = ContactInfo(type='email', value='invalid-email')
            contact.full_clean()
        with self.assertRaises(ValidationError):
            contact = ContactInfo(type='phone', value='123')
            contact.full_clean()
        with self.assertRaises(ValidationError):
            contact = ContactInfo(type='linkedin', value='invalid-url')
            contact.full_clean()
        with self.assertRaises(ValidationError):
            contact = ContactInfo(type='invalid_type', value='some_value')
            contact.full_clean()

    def test_contact_icon_fallback(self):
        contact = ContactInfo(type='facebook', value='https://facebook.com/user')
        self.assertEqual(contact.icon, 'fab fa-facebook')
        contact.type = 'unknown'
        self.assertEqual(contact.icon, 'fas fa-address-card')
        self.assertEquals(self.category.name, 'Programming Languages')
        self.assertTrue(isinstance(self.category, SkillCategory))
        self.assertEqual(str(self.category), 'Programming Languages')

class SkillModelTest(TestCase):
    def setUp(self):
        self.category = SkillCategory.objects.create(name='Programming Languages')
        self.skill = Skill.objects.create(name='Python', category=self.category)

    def test_skill_creation(self):
        self.assertEquals(self.skill.name, 'Python')
        self.assertTrue(isinstance(self.skill, Skill))
        self.assertEqual(str(self.skill), 'Python')
        self.assertEqual(self.skill.category, self.category)

class LanguageProficiencyModelTest(TestCase):
    def setUp(self):
        self.language = LanguageProficiency.objects.create(
            language='English',
            proficiency='B1'
        )
    
    def test_language_proficiency_creation(self):
        self.assertEquals(self.language.language, 'English')
        self.assertEquals(self.language.proficiency, 'B1')
        self.assertTrue(isinstance(self.language, LanguageProficiency))
        self.assertEqual(str(self.language), 'English (B1)')
        
class EducationModelTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            institution='FAST - UAC',
            degree='Bachelier en Mathématiques Fondamentales',
            start_date='2020-09-01',
            end_date='2023-07-01',
            location='Paris, France',
            description='Description of the education'
        )
        
    def test_education_creation(self):
        self.assertEquals(self.education.institution, 'FAST - UAC')
        self.assertEquals(self.education.degree, 'Bachelier en Mathématiques Fondamentales')
        self.assertEquals(self.education.start_date, '2020-09-01')
        self.assertEquals(self.education.end_date, '2023-07-01')
        self.assertEquals(self.education.location, 'Paris, France')
        self.assertEquals(self.education.description, 'Description of the education')
        self.assertTrue(isinstance(self.education, Education))
        self.assertEqual(str(self.education), 'Bachelier en Mathématiques Fondamentales at FAST - UAC')
        
class ExperienceModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='AI')
        self.experience = Experience.objects.create(
            title='Data Scientist',
            company='Tech Company',
            role_type='Professional',
            start_date='2024-01-01',
            end_date='2024-12-31',
            location='Cotonou, Bénin',
            description='Description du poste'
        )
        self.experience.tags.add(self.tag)

    def test_experience_creation(self):
        self.assertEqual(self.experience.title, 'Data Scientist')
        self.assertEqual(self.experience.company, 'Tech Company')
        self.assertEqual(self.experience.role_type, 'Professional')
        self.assertEqual(str(self.experience), 'Data Scientist at Tech Company')
        self.assertTrue(self.experience.tags.filter(name='AI').exists())

class ProjectModelTest(TestCase):
    def setUp(self):
        self.category = SkillCategory.objects.create(name='AI')
        self.skill = Skill.objects.create(name='PyTorch', category=self.category)
        self.tag = Tag.objects.create(name='Deep Learning')
        self.project = Project.objects.create(
            title='Isheero',
            context='Research',
            start_date='2024-01-01',
            end_date='2024-12-31',
            location='Bénin',
            description='Système d\'annotation d\'images',
            github_link='https://github.com/yemal22/isheero'
        )
        self.project.technologies.add(self.skill)
        self.project.tags.add(self.tag)

    def test_project_creation(self):
        self.assertEqual(self.project.title, 'Isheero')
        self.assertEqual(str(self.project), 'Isheero')
        self.assertTrue(self.project.technologies.filter(name='PyTorch').exists())
        self.assertTrue(self.project.tags.filter(name='Deep Learning').exists())

class CertificationModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Data Science')
        self.certification = Certification.objects.create(
            name='Data Science Professional Certificate',
            provider='IBM',
            date_issued='2024-01-01',
            description='Formation complète en Data Science',
            link='https://www.coursera.org/certificate/123'
        )
        self.certification.tags.add(self.tag)

    def test_certification_creation(self):
        self.assertEqual(self.certification.name, 'Data Science Professional Certificate')
        self.assertEqual(self.certification.provider, 'IBM')
        self.assertTrue(self.certification.tags.filter(name='Data Science').exists())

class ContactInfoModelTest(TestCase):
    def setUp(self):
        self.email_contact = ContactInfo.objects.create(
            type='email',
            value='yemalem03@gmail.com'
        )
        self.phone_contact = ContactInfo.objects.create(
            type='phone',
            value='+22995754157'
        )
        self.linkedin_contact = ContactInfo.objects.create(
            type='linkedin',
            value='https://www.linkedin.com/in/morel-kpavode'
        )

    def test_contact_info_creation(self):
        self.assertEqual(str(self.email_contact), 'Email: yemalem03@gmail.com')
        self.assertEqual(str(self.phone_contact), 'Phone: +22995754157')
        self.assertEqual(str(self.linkedin_contact), 'Linkedin: https://www.linkedin.com/in/morel-kpavode')

    def test_contact_icon_property(self):
        self.assertEqual(self.email_contact.icon, 'fas fa-envelope')
        self.assertEqual(self.phone_contact.icon, 'fas fa-phone')
        self.assertEqual(self.linkedin_contact.icon, 'fab fa-linkedin')

    def test_invalid_contact_values(self):
        with self.assertRaises(ValidationError):
            contact = ContactInfo(type='email', value='invalid-email')
            contact.full_clean()

        with self.assertRaises(ValidationError):
            contact = ContactInfo(type='phone', value='123')
            contact.full_clean()

        with self.assertRaises(ValidationError):
            contact = ContactInfo(type='linkedin', value='invalid-url')
            contact.full_clean()

        with self.assertRaises(ValidationError):
            contact = ContactInfo(type='invalid_type', value='some_value')
            contact.full_clean()