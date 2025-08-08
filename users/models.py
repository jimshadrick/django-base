from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    CustomUser is an extension of the default AbstractUser model tailored for additional
    functionality and attributes relevant to a specific application.

    This class introduces a custom field to track the data consent date and overrides
    certain model attributes from the parent AbstractUser model. It also modifies the default
    required fields for user creation and is configurable through its Meta class.

    Attributes
    ----------
    data_consent_date : DateField
        Stores the date when the user provided consent for data usage.

    REQUIRED_FIELDS : list of str
        Specifies fields that are required when creating a user instance.
    """
    data_consent_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date when data consent was given')
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
