from django import forms
from django.contrib.auth.models import User
from .models import linksModel


class linksForm(forms.ModelForm):
    class Meta:
        model = linksModel
        fields = ['url', 'title']
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

class linkEditForm(forms.ModelForm):
    class Meta:
        model = linksModel
        fields = ['url', 'title', ]
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }