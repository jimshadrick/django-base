from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse
from django.utils.html import format_html

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Defines a custom user creation form that inherits 
    from Django's built-in `UserCreationForm`. The form 
    is associated with the `CustomUser` model and includes 
    all the fields from the original `UserCreationForm`.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    """
    Defines a custom user change form that inherits 
    from Django's built-in `UserChangeForm`. The form 
    is associated with the `CustomUser` model and includes 
    all the fields from the original `UserChangeForm`.
    """

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class UserProfileForm(forms.ModelForm):
    """Form for users to update their profile information"""

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'display_name']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'readonly': 'readonly',
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display Name (optional)',
            }),
        }

        help_texts = {
            'display_name': 'Leave blank to automatically use your full name.'
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set dynamic help text for the email field.
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = format_html(
            'To change your email, use the <a href="{}">Email management page</a>.',
            reverse('account_email')
        )

    def clean_email(self):
        """Prevent email from being changed via this form"""
        return self.instance.email
