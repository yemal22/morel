from django.test import TestCase, Client
from django.urls import reverse
from portfolio.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, mock_open

class HomeViewTest(TestCase):
    """Test suite for the home page view functionality.
    Verifies both the response status and template usage."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def _get_home_response(self):
        """Helper method to get response from home page."""
        return self.client.get(self.url)

    def test_should_return_success_status(self):
        response = self._get_home_response()
        self.assertEquals(response.status_code, 200)

    def test_should_use_correct_template(self):
        response = self._get_home_response()
        self.assertTemplateUsed(response, 'home.html')


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')
        ContactInfo.objects.create(type='Email', value='test@example.com')

    def test_should_render_contact_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    @patch('portfolio.views.send_mail')
    def test_should_send_mail_on_valid_post(self, mock_send_mail):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Hello!'
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertTrue(mock_send_mail.called)
        self.assertContains(response, "Message sent successfully")

    def test_should_show_error_on_invalid_post(self):
        response = self.client.post(self.url, {}, follow=True)
        self.assertContains(response, "There was an error sending your message")


class ProjectListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('project-list')
        Project.objects.create(title='Test Project', start_date='2020-01-01')

    def test_should_render_projects_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')
        self.assertContains(response, 'Test Project')


class ProjectJsonViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(title='Json Project', start_date='2020-01-01')
        self.url = reverse('project-json', args=[self.project.pk])

    def test_should_return_project_json(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('title', response.json())


class SkillListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('skills')
        category = SkillCategory.objects.create(name='Programming')
        Skill.objects.create(name='Python', category=category)

    def test_should_render_skills_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'skills.html')
        self.assertContains(response, 'Python')


class CertificationListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('certifications')
        Certification.objects.create(name='Cert1', provider='Provider', date_issued='2022-01-01', is_primary=True)

    def test_should_render_certifications_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'certifications.html')
        self.assertContains(response, 'Cert1')


class EducationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('education')
        Education.objects.create(
            degree='BSc',  # Use the correct field name here
            institution='Uni',
            start_date='2018-01-01',
            end_date='2022-01-01'
        )

    def test_should_render_education_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education.html')
        self.assertContains(response, 'BSc')


class GenerateCVPDFViewTest(TestCase):
    @patch('portfolio.views.render_to_string', return_value='\\documentclass{article}\\begin{document}Test CV\\end{document}')
    @patch('portfolio.views.subprocess.run')
    @patch('portfolio.views.open', create=True)
    def test_generate_cv_pdf(self, mock_open_func, mock_subprocess, mock_render_to_string):
        # Mock for writing (tex file)
        m = mock_open()
        # Mock for reading (pdf file)
        m_pdf = mock_open(read_data=b"PDFDATA")
        # open() returns m() for writing, m_pdf() for reading
        def open_side_effect(file, mode='r', *args, **kwargs):
            if 'w' in mode:
                return m()
            elif 'r' in mode or 'b' in mode:
                return m_pdf()
            else:
                return m()
        mock_open_func.side_effect = open_side_effect

        client = Client()
        url = reverse('resume')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

