from django import forms
from django.contrib.auth.models import User
from typing import Any, Dict
from .models import Post, Comment, Profile, Card
from django.forms.widgets import FileInput

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError("Email is already registered")

        return cleaned_data


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match.')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'pronouns', 'bio']
        exclude = ['user']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class PronounsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pronouns']

class BioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pronouns', 'bio']



class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['title', 'subtitle', 'image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter description...'})
        }