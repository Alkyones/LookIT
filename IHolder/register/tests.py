from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .views import register, profile
from .forms import NewRegisterForm

class RegisterProfileTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_register_valid_form(self):
        # Create a POST request with valid form data
        request = self.factory.post('/register/', {
            'username': 'john',
            'email': 'joh321n@gmail.com',
            'password1': 'secret',
            'password2': 'secret'
        })
        response = register(request)

        # Check that the form is saved
        self.assertEqual(response.status_code, 200)
        self.assertTrue(NewRegisterForm(request.POST))


    def test_register_invalid_form(self):
        # Create a POST request with invalid form data
        request = self.factory.post('/register/', {
            'username': 'john',
            'email': 'invalid_email',
            'password': 'secret'
        })
        response = register(request)

        # Check that the form is not saved
        self.assertEqual(response.status_code, 200)
        self.assertFalse(NewRegisterForm(request.POST).is_valid())

