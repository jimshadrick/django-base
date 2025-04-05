from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Defines a custom user creation form that inherits 
    from Django's built-in `UserCreationForm`. The form 
    is associated with the `CustomUser` model and includes 
    all the fields from the original `UserCreationForm` 
    plus an additional field called `is_email_confirmed`.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('is_email_confirmed',)


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
