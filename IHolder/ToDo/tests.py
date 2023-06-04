from django.test import TestCase
from django.contrib.auth.models import User
from .models import TodoList, TodoListItem
from datetime import datetime

class TodoListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Alkyone2', password='asdwer123')
        self.todo_list = TodoList.objects.create(name='Test List', user=self.user)
        
    def test_todo_list_name(self):
        self.assertEqual(self.todo_list.name, 'Test List')
        
    def test_todo_list_user(self):
        self.assertEqual(self.todo_list.user, self.user)

class TodoListItemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Alkyone2', password='asdwer123')
        self.todo_list = TodoList.objects.create(name='Test List', user=self.user)
        self.todo_list_item = TodoListItem.objects.create(content='Test Item', todo_list=self.todo_list)
        
    def test_todo_list_item_content(self):
        self.assertEqual(self.todo_list_item.content, 'Test Item')
        
    def test_todo_list_item_todo_list(self):
        self.assertEqual(self.todo_list_item.todo_list, self.todo_list)
        
    def test_todo_list_item_is_completed_default_false(self):
        self.assertFalse(self.todo_list_item.is_completed)
