from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from Itracker.forms import searchForm
from eventTracker.models import searchSavedEvents, userSavedEventsModel, SavedEvents

from eventTracker.views import eventTrackerMain

class EventTrackerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_eventTrackerMain(self):
        # Create a POST request with a valid form
        response = self.client.post('/events/', {'searchQuery': 'technology'})
        
        # Assert that the response has a successful status code
        self.assertEqual(response.status_code, 200)
        
        # Assert that the saved events for the user are retrieved correctly
        saved_user_events = userSavedEventsModel.objects.filter(user=self.user).values_list("title", flat=True)
        self.assertQuerysetEqual(response.context['savedEvents'], saved_user_events, transform=str)
        
        # Assert that the search results are rendered correctly
        self.assertTemplateUsed(response, 'eventTracker/search.html')
        
        # Assert that the search form is reset
        self.assertIsInstance(response.context['form'], searchForm)

        # Assert that the events are saved correctly
        search_saved_events = searchSavedEvents.objects.all()
        

        # Assert the response behavior for the invalid form case
        self.assertEqual(len(search_saved_events), 10)  # Assuming no events were found
        
     


class ModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_searchSavedEvents_model(self):
        event = searchSavedEvents.objects.create(
            title='Event Title',
            description='Event Description',
            eventDate='2023-05-20',
            link='https://example.com',
            online=True
        )

        self.assertEqual(event.title, 'Event Title')
        self.assertEqual(event.description, 'Event Description')
        self.assertEqual(event.eventDate, '2023-05-20')
        self.assertEqual(event.link, 'https://example.com')
        self.assertTrue(event.online)

        # Test __str__ method
        self.assertEqual(str(event), 'Event Title')

    def test_userSavedEventsModel_model(self):
        event = userSavedEventsModel.objects.create(
            title='Event Title',
            description='Event Description',
            eventDate='2023-05-20',
            link='https://example.com',
            online=True,
            user=self.user
        )

        self.assertEqual(event.title, 'Event Title')
        self.assertEqual(event.description, 'Event Description')
        self.assertEqual(event.eventDate, '2023-05-20')
        self.assertEqual(event.link, 'https://example.com')
        self.assertTrue(event.online)
        self.assertEqual(event.user, self.user)


    def test_SavedEvents_model(self):
        event = SavedEvents.objects.create(
            title='Event Title',
            timeEvent='2023-05-20',
            image='https://example.com/image.jpg',
            link='https://example.com',
            publisher='Publisher Name'
        )

        self.assertEqual(event.title, 'Event Title')
        self.assertEqual(event.timeEvent, '2023-05-20')
        self.assertEqual(event.image, 'https://example.com/image.jpg')
        self.assertEqual(event.link, 'https://example.com')
        self.assertEqual(event.publisher, 'Publisher Name')

        # Test __str__ method
        self.assertEqual(str(event), 'Event Title')



class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_savedUserEvents_view_authenticated(self):
        # Simulate an authenticated user
        self.client.login(username='testuser', password='testpassword')

        # Create a saved event for the user
        saved_event = userSavedEventsModel.objects.create(
            title='Event Title',
            description='Event Description',
            eventDate='2023-05-20',
            link='https://example.com',
            online=True,
            user=self.user
        )

        # Make a GET request to the view
        response = self.client.get(reverse('saved-events'))

        # Assert that the response has a successful status code
        self.assertEqual(response.status_code, 200)

        # Assert that the saved event is rendered correctly in the template
        self.assertContains(response, 'Event Title')

        # Assert that the correct template is used
        self.assertTemplateUsed(response, 'eventTracker/savedEvents.html')


