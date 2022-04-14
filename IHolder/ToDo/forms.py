from django import forms
from .models import TodoList, TodoListItem



class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['name']

class TodoListItemForm(forms.ModelForm):
    class Meta:
        model = TodoListItem
        fields = ['content', 'is_completed']