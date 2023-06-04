from django.test import Client, TestCase
from django.contrib.auth.models import User
from AI.models import AIChatModelNew

class ChatViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='Alkyone2', password='asdwer123')

    def test_chat_post_request(self):
        # Log in the user
        self.client.login(username='Alkyone2', password='asdwer123')
        
        # Send a POST request to the chat view
        response = self.client.post('/ai/chat/', {'keyword': 'test keyword'})
        
        # Assert that the response has a successful status code (e.g., 200)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the chat result was saved for the user
        self.assertTrue(AIChatModelNew.objects.filter(user=self.user, keyword='test keyword'))

    def test_chat_get_request(self):
        # Log in the user
        self.client.login(username='Alkyone2', password='asdwer123')

        # Send a GET request to the chat view
        response = self.client.get('/ai/chat/')

        # Assert that the response has a successful status code (e.g., 200)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the user's search results are included in the response
        self.assertContains(response, self.user.username)

