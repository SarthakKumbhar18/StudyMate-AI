from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class RegistrationForm(UserCreationForm):

    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('TUTOR', 'Tutor'),
    ]

    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2', 'role']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )

        return email


class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'autofocus': True
        })
    )
    
    
    
    
class StudentProfileForm(forms.ModelForm):
    
    class Meta:
        model = StudentProfile
        fields = [
            'phone',
            'profile_picture',
            'college',
            'course',
            'year',
            'education_details',
            'skills',
            'interests'
        ]

        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter phone number'
            }),
            'college': forms.TextInput(attrs={
                'placeholder': 'Enter college name'
            }),
            'course': forms.TextInput(attrs={
                'placeholder': 'Enter course'
            }),
            'education_details': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter education details'
            }),
            'skills': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Python, Django, SQL'
            }),
            'interests': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter your interests'
            }),
        }