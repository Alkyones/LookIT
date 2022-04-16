from logging import PlaceHolder
from django import forms
from .models import TodoList, TodoListItem



class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['name']

class TodoListItemForm(forms.ModelForm):
    content = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Enter a task'}))
    class Meta:
        model = TodoListItem
        fields = ['content']
        
        