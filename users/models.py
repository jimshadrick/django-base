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
    """

    display_name = models.CharField(max_length=100, blank=True, null=True)

    @property
    def get_display_name(self):
        return self.display_name or self.get_full_name() or self.email.split('@')[0]

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
