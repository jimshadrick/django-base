from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Defines a custom admin interface for the CustomUser model.
    Specify the custom forms to use for creating and editing 
    users, the fields to display in the admin list view, and 
    the fields to include in the detail view. 
    The CustomUserAdmin class inherits from Django's built-in 
    UserAdmin class and customizes its behavior.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active', 'data_consent_date']
    list_filter = ['email', 'is_staff', 'is_active', ]
    fieldsets = (
            UserAdmin.fieldsets + (
        (None, {'fields': ('data_consent_date',)}),
    )
    )
    add_fieldsets = (
            UserAdmin.add_fieldsets + (
        (None, {'fields': ('data_consent_date',)}),
    )
    )
    search_fields = ['email']
    ordering = ['email']


admin.site.register(CustomUser, CustomUserAdmin)
