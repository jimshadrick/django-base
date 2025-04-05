from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom User Model - Extends AbstractUser and adds email_confirmed field
    AbstractUser is a subclass of `AbstractBaseUser` and `PermissionsMixin` 
    that provides a fully functional user model out of the box.
    """
    is_email_confirmed = models.BooleanField(_('Email Confirmed'), default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
