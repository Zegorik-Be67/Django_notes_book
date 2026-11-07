from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Notes, Tags


class NotesForm(ModelForm):
    class Meta:
        model = Notes
        fields = ['tags', 'note']
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }

class TagsForm(ModelForm):
    class Meta:
        model = Tags
        fields = ['name']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())