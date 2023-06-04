from django.test import TestCase, Client
from django.urls import reverse
from .models import linksModel
from .forms import linksForm, linkEditForm
from django.contrib.auth.models import User


class LinksaverTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('index')

    def test_linksaverIndex_post(self):
        form_data = {
            'url': 'http://example.com',
            'title': 'Example',
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)

        links = linksModel.objects.filter(user=self.user)
        self.assertEqual(links.count(), 1)
        self.assertEqual(links.first().url, form_data['url'])
        self.assertEqual(links.first().title, form_data['title'])

    def test_linksaverDelete(self):
        link = linksModel.objects.create(user=self.user, url='http://example.com', title='Example')
        delete_url = reverse('delete', args=[link.id])

        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 302)

        links = linksModel.objects.filter(user=self.user)
        self.assertEqual(links.count(), 0)

    def test_linksaverEdit(self):
        link = linksModel.objects.create(user=self.user, url='http://example.com', title='Example')
        edit_url = reverse('edit', args=[link.id])

        form_data = {
            'url': 'http://example.org',
            'title': 'New Example',
        }

        response = self.client.post(edit_url, form_data)
        self.assertEqual(response.status_code, 302)

        link.refresh_from_db()
        self.assertEqual(link.url, form_data['url'])
        self.assertEqual(link.title, form_data['title'])
